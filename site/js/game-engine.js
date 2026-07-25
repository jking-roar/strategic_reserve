export const SIZE = 6;
export const RED = "RED";
export const BLUE = "BLUE";

const INITIAL_ROWS = ["......", ".RBRB.", ".B..R.", ".R..B.", ".BRBR.", "......"];
const other = player => player === RED ? BLUE : RED;
const key = ([row, col]) => `${row},${col}`;
const inside = (row, col) => row >= 0 && row < SIZE && col >= 0 && col < SIZE;
const neighbours = ([row, col]) => [[row-1,col],[row+1,col],[row,col-1],[row,col+1]].filter(([r,c]) => inside(r,c));

export function createGame() {
  return { board: INITIAL_ROWS.map(row => [...row].map(v => v === "R" ? RED : v === "B" ? BLUE : null)), reserves:{RED:6,BLUE:6}, currentPlayer:RED, phase:"await-roll", dice:null, target:null, legalMoves:[], winner:null, turn:1, message:"Red's turn. Roll the dice." };
}
export function cloneState(state) { return { ...state, board:state.board.map(row=>[...row]), reserves:{...state.reserves}, dice:state.dice&&{...state.dice}, target:state.target&&[...state.target], legalMoves:state.legalMoves.map(move=>[...move]) }; }
export function rollDie(random=Math.random) { const value=Number(random());const normalized=Number.isFinite(value)?Math.min(Math.max(value,0),1-Number.EPSILON):0;return 1+Math.floor(normalized*SIZE); }
export function perspectiveTarget(player, column, row) {
  if (![column,row].every(value => Number.isInteger(value) && value >= 1 && value <= 6)) throw new RangeError("Dice values must be integers from 1 through 6.");
  return player === RED ? [SIZE-row,column-1] : [row-1,SIZE-column];
}
export function groupAt(board, start) {
  const color=board[start[0]]?.[start[1]]; if (!color) return [];
  const found=[], seen=new Set([key(start)]), pending=[start];
  while(pending.length){ const point=pending.pop(); found.push(point); for(const next of neighbours(point)){ if(board[next[0]][next[1]]===color&&!seen.has(key(next))){seen.add(key(next));pending.push(next);} } }
  return found;
}
export function groups(board, color) {
  const result=[], seen=new Set();
  for(let row=0;row<SIZE;row++) for(let col=0;col<SIZE;col++) if(board[row][col]===color&&!seen.has(key([row,col]))){const group=groupAt(board,[row,col]);group.forEach(p=>seen.add(key(p)));result.push(group);}
  return result;
}
function emptySquares(board){ const result=[];for(let r=0;r<SIZE;r++)for(let c=0;c<SIZE;c++)if(!board[r][c])result.push([r,c]);return result; }
function removeGroup(state, group, owner){ group.forEach(([r,c])=>state.board[r][c]=null);state.reserves[owner]+=group.length;return group.length; }
export function resolveRoll(input, column, row) {
  if(input.phase!=="await-roll"||input.winner) throw new Error("Dice cannot be rolled now.");
  const state=cloneState(input), player=state.currentPlayer, enemy=other(player), target=perspectiveTarget(player,column,row), occupant=state.board[target[0]][target[1]];
  state.dice={column,row};state.target=target;let captured=0,kind="empty", friendly=[];
  if(occupant===enemy){ kind="enemy";captured=removeGroup(state,groupAt(state.board,target),enemy); }
  else if(occupant===player){ kind="friendly";friendly=groupAt(state.board,target);const enemyPoints=new Set();for(const point of friendly)for(const adjacent of neighbours(point))if(state.board[adjacent[0]][adjacent[1]]===enemy)groupAt(state.board,adjacent).forEach(p=>enemyPoints.add(key(p)));const capturedPoints=[...enemyPoints].map(v=>v.split(",").map(Number));captured=removeGroup(state,capturedPoints,enemy); }
  state.legalMoves=kind==="friendly" ? [...new Map(friendly.flatMap(neighbours).filter(([r,c])=>!state.board[r][c]).map(p=>[key(p),p])).values()] : emptySquares(state.board);
  if(state.reserves[player] <= 0) state.legalMoves=[];
  state.phase=state.legalMoves.length?"await-placement":"await-pass";
  const action=state.legalMoves.length?`${state.legalMoves.length} legal placement${state.legalMoves.length===1?"":"s"}.`:"No legal placement. Acknowledge to pass.";
  state.message=`${player === RED ? "Red" : "Blue"} rolled column ${column}, row ${row}; ${kind} target${captured?`, captured ${captured}`:""}. ${action}`;
  return state;
}
export function place(input, coordinate) {
  if(input.phase!=="await-placement"||input.winner) throw new Error("A checker cannot be placed now.");
  if(!input.legalMoves.some(([r,c])=>r===coordinate[0]&&c===coordinate[1])) throw new Error("That square is not a legal placement.");
  const state=cloneState(input),player=state.currentPlayer;state.board[coordinate[0]][coordinate[1]]=player;state.reserves[player]--;
  if(state.reserves[player]===0){state.winner=player;state.phase="game-over";state.legalMoves=[];state.message=`${player === RED ? "Red" : "Blue"} wins!`;return state;}
  return nextTurn(state,`${player === RED ? "Red" : "Blue"} placed a checker.`);
}
export function pass(input) { if(input.phase!=="await-pass"||input.winner) throw new Error("The turn cannot be passed now.");return nextTurn(cloneState(input),`${input.currentPlayer === RED ? "Red" : "Blue"} acknowledged no legal play and passed.`); }
function nextTurn(state,prefix){state.currentPlayer=other(state.currentPlayer);state.phase="await-roll";state.dice=null;state.target=null;state.legalMoves=[];state.turn++;state.message=`${prefix} ${state.currentPlayer === RED ? "Red" : "Blue"}'s turn.`;return state;}
export function isLegalMove(state, move){return Array.isArray(move)&&state.phase==="await-placement"&&state.legalMoves.some(([r,c])=>r===move[0]&&c===move[1]);}
