import { BLUE, RED, cloneState, isLegalMove, place, resolveRoll } from "./game-engine.js";

export function randomIndex(length, random=Math.random) { if(!Number.isInteger(length)||length<1)throw new RangeError("Length must be positive.");const value=Number(random());const normalized=Number.isFinite(value)?Math.min(Math.max(value,0),1-Number.EPSILON):0;return Math.floor(normalized*length); }
const randomItem=(items,random)=>items[randomIndex(items.length,random)];
export function chooseRudimentaryMove(state, random=Math.random){const snapshot=cloneState(state);return snapshot.legalMoves.length?[...randomItem(snapshot.legalMoves,random)]:null;}

function scoreMove(state, move, player) {
  const opponent=player===RED?BLUE:RED;let score=(state.reserves[opponent]-state.reserves[player])*20;
  const [r,c]=move;score += (5-Math.abs(2.5-r)-Math.abs(2.5-c));
  for(const [dr,dc] of [[-1,0],[1,0],[0,-1],[0,1]]) if(state.board[r+dr]?.[c+dc]===player) score+=3;
  return score;
}
export function chooseAdvancedMove(state, options={}) {
  const now=options.now||(()=>performance.now()), started=now(), budget=options.budgetMs??4900, player=state.currentPlayer, moves=state.legalMoves.map(v=>[...v]);
  if(!moves.length)return null;let best=moves[0],bestScore=-Infinity;
  candidateLoop: for(const move of moves){if(now()-started>=budget)break;let score=scoreMove(state,move,player);
    // Use the authoritative transition. A terminal move needs no reply analysis.
    const simulated=place(state,move);
    if(simulated.winner===player) score=Number.MAX_SAFE_INTEGER;
    else {
      // Once evaluation starts, finish all 36 equally likely outcomes for this candidate.
      for(let column=1;column<=6;column++)for(let row=1;row<=6;row++){if(now()-started>=budget)break candidateLoop;const outcome=resolveRoll(simulated,column,row);options.onOutcome?.({move:[...move],column,row});score-=outcome.legalMoves.length/36;score-=(outcome.reserves[player]-simulated.reserves[player])*12/36;}
    }
    if(score>bestScore){bestScore=score;best=move;}
  }
  return isLegalMove(state,best)?[...best]:null;
}
