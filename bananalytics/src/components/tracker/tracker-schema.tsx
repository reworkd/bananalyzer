export const NUM_RUNS_PER_EXAMPLE = 50;

export type Example = {
  id: number;
  url: string;
};
export type ExampleRun = {
  id: number;
  background: string;
};

export type ExampleWithRuns = Example & {
  runs: ExampleRun[];
}
