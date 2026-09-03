// Deliberately not wired in the first vertical slice.
// Score persistence comes after the combat loop is stable.
export type ScoreSubmission = {
  runId: string;
  score: number;
  kills: number;
  nickname: string;
  country: string;
};

export async function submitScore(_score: ScoreSubmission): Promise<void> {
  throw new Error('Leaderboard transport is not enabled in Build 1.0-alpha.1');
}
