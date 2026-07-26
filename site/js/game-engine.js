export const SIZE = 6;
export const RED = "RED";
export const BLUE = "BLUE";
const PLAYERS=[RED,BLUE], TOTAL=12;
const INITIAL_ROWS = ["......", ".RBRB.", ".B..R.", ".R..B.", ".BRBR.", "......"];
const other = player => player === RED ? BLUE : RED;
const key = ([row, col]) => `${row},${col}`;
const inside = (row, col) => Number.isInteger(row)&&Number.isInteger(col)&&row >= 0 && row < SIZE && col >= 0 && col < SIZE;
const neighbours = ([row, col]) => [[row-1,col],[row+1,col],[row,col-1],[row,col+1]].filter(([r,c]) => inside(r,c));
const fail=message=>{throw new Error(`Invalid game state: ${message}`);};
export function perspectiveTarget(player,column,row){
  if(!PLAYERS.includes(player))throw new RangeError("Player must be RED or BLUE.");
  if(![column,row].every(value=>Number.isInteger(value)&&value>=1&&value<=SIZE))throw new RangeError("Dice values must be integers from 1 through 6.");
  return player===RED?[SIZE-row,column-1]:[row-1,SIZE-column];
}
export function validateGameState(state){
  if(!state||!Array.isArray(state.board)||state.board.length!==SIZE||state.board.some(row=>!Array.isArray(row)||row.length!==SIZE))fail("board must be 6x6.");
  if(state.board.flat().some(cell=>cell!==null&&!PLAYERS.includes(cell)))fail("board contains an invalid token.");
  if(!PLAYERS.includes(state.currentPlayer))fail("current player must be RED or BLUE.");
  if(!state.reserves||Object.keys(state.reserves).sort().join(",")!=="BLUE,RED")fail("reserves must contain RED and BLUE.");
  for(const player of PLAYERS){const reserve=state.reserves[player],count=state.board.flat().filter(cell=>cell===player).length;if(!Number.isInteger(reserve)||reserve<0||reserve>TOTAL||count+reserve!==TOTAL)fail("board and reserves must conserve twelve checkers per player.");}
  const empty=PLAYERS.filter(player=>state.reserves[player]===0);
  if(empty.length>1||(empty.length&&state.winner!==empty[0])||(!empty.length&&state.winner!==null))fail("winner must be the sole player with an empty reserve.");
  if(!Number.isInteger(state.turn)||state.turn<1)fail("turn must be a positive integer.");
  if(!Array.isArray(state.legalMoves))fail("legal moves must be an array.");
  if(state.phase==="await-roll"){
    if(state.winner!==null||state.dice!==null||state.target!==null||state.legalMoves.length)fail("await-roll context is incoherent.");
  }else if(state.phase==="await-placement"){
    if(state.winner!==null||!state.dice||!Array.isArray(state.target)||state.target.length!==2||!state.legalMoves.length)fail("a resolved active turn requires legal placements.");
    let expected;try{expected=perspectiveTarget(state.currentPlayer,state.dice.column,state.dice.row);}catch{fail("resolved dice are invalid.");}
    if(!state.target.every(Number.isInteger)||key(expected)!==key(state.target))fail("target must contain integer coordinates matching the dice.");
    const seen=new Set();for(const move of state.legalMoves){if(!Array.isArray(move)||move.length!==2||!inside(...move)||seen.has(key(move))||state.board[move[0]][move[1]]!==null)fail("legal moves must be unique empty in-bounds squares.");seen.add(key(move));}
  }else if(state.phase==="game-over"){
    if(!state.winner||state.currentPlayer!==state.winner||state.dice!==null||state.target!==null||state.legalMoves.length)fail("completed game context is incoherent.");
  }else fail("phase is invalid.");
  return state;
}
export function createGame(){const state={board:INITIAL_ROWS.map(row=>[...row].map(v=>v==="R"?RED:v==="B"?BLUE:null)),reserves:{RED:6,BLUE:6},currentPlayer:RED,phase:"await-roll",dice:null,target:null,legalMoves:[],winner:null,turn:1,message:"Red's turn. Roll the dice."};return validateGameState(state);}
export function cloneState(state){return{...state,board:state.board.map(row=>[...row]),reserves:{...state.reserves},dice:state.dice&&{...state.dice},target:state.target&&[...state.target],legalMoves:state.legalMoves.map(move=>[...move])};}
export function rollDie(random=Math.random){const value=Number(random());const normalized=Number.isFinite(value)?Math.min(Math.max(value,0),1-Number.EPSILON):0;return 1+Math.floor(normalized*SIZE);}
export function groupAt(board,start){const color=board[start[0]]?.[start[1]];if(!color)return[];const found=[],seen=new Set([key(start)]),pending=[start];while(pending.length){const point=pending.pop();found.push(point);for(const next of neighbours(point))if(board[next[0]][next[1]]===color&&!seen.has(key(next))){seen.add(key(next));pending.push(next);}}return found;}
export function groups(board,color){const result=[],seen=new Set();for(let row=0;row<SIZE;row++)for(let col=0;col<SIZE;col++)if(board[row][col]===color&&!seen.has(key([row,col]))){const group=groupAt(board,[row,col]);group.forEach(p=>seen.add(key(p)));result.push(group);}return result;}
function emptySquares(board){const result=[];for(let r=0;r<SIZE;r++)for(let c=0;c<SIZE;c++)if(!board[r][c])result.push([r,c]);return result;}
function removeGroup(state,group,owner){group.forEach(([r,c])=>state.board[r][c]=null);state.reserves[owner]+=group.length;return group.length;}
export function resolveRoll(input,column,row){validateGameState(input);if(input.phase!=="await-roll"||input.winner)throw new Error("Dice cannot be rolled now.");const state=cloneState(input),player=state.currentPlayer,enemy=other(player),target=perspectiveTarget(player,column,row),occupant=state.board[target[0]][target[1]];state.dice={column,row};state.target=target;let captured=0,kind="empty",friendly=[];if(occupant===enemy){kind="enemy";captured=removeGroup(state,groupAt(state.board,target),enemy);}else if(occupant===player){kind="friendly";friendly=groupAt(state.board,target);const enemyPoints=new Set();for(const point of friendly)for(const adjacent of neighbours(point))if(state.board[adjacent[0]][adjacent[1]]===enemy)groupAt(state.board,adjacent).forEach(p=>enemyPoints.add(key(p)));captured=removeGroup(state,[...enemyPoints].map(v=>v.split(",").map(Number)),enemy);}state.legalMoves=kind==="friendly"?[...new Map(friendly.flatMap(neighbours).filter(([r,c])=>!state.board[r][c]).map(p=>[key(p),p])).values()]:emptySquares(state.board);if(!state.legalMoves.length)fail("a valid active roll must produce a legal placement.");state.phase="await-placement";state.message=`${player===RED?"Red":"Blue"} rolled column ${column}, row ${row}; ${kind} target${captured?`, captured ${captured}`:""}. ${state.legalMoves.length} legal placement${state.legalMoves.length===1?"":"s"}.`;return validateGameState(state);}
export function place(input,coordinate){validateGameState(input);if(input.phase!=="await-placement"||input.winner)throw new Error("A checker cannot be placed now.");if(!Array.isArray(coordinate)||!input.legalMoves.some(([r,c])=>r===coordinate[0]&&c===coordinate[1]))throw new Error("That square is not a legal placement.");const state=cloneState(input),player=state.currentPlayer;state.board[coordinate[0]][coordinate[1]]=player;state.reserves[player]--;if(state.reserves[player]===0){state.winner=player;state.phase="game-over";state.dice=null;state.target=null;state.legalMoves=[];state.message=`${player===RED?"Red":"Blue"} wins!`;return validateGameState(state);}return validateGameState(nextTurn(state,`${player===RED?"Red":"Blue"} placed a checker.`));}
function nextTurn(state,prefix){state.currentPlayer=other(state.currentPlayer);state.phase="await-roll";state.dice=null;state.target=null;state.legalMoves=[];state.turn++;state.message=`${prefix} ${state.currentPlayer===RED?"Red":"Blue"}'s turn.`;return state;}
export function isLegalMove(state,move){return Array.isArray(move)&&state.phase==="await-placement"&&state.legalMoves.some(([r,c])=>r===move[0]&&c===move[1]);}
