export type RunSnapshot = {
  runId: string;
  score: number;
  kills: number;
  startedAt: number;
  endedAt: number;
};

class RunStateStore {
  runId = '';
  score = 0;
  kills = 0;
  startedAt = 0;
  endedAt = 0;

  reset(): void {
    this.runId = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    this.score = 0;
    this.kills = 0;
    this.startedAt = Date.now();
    this.endedAt = 0;
  }

  addKill(points = 100): void {
    this.kills += 1;
    this.score += points;
  }

  finish(): RunSnapshot {
    this.endedAt = Date.now();
    return this.snapshot();
  }

  snapshot(): RunSnapshot {
    return {
      runId: this.runId,
      score: this.score,
      kills: this.kills,
      startedAt: this.startedAt,
      endedAt: this.endedAt,
    };
  }
}

export const RunState = new RunStateStore();
