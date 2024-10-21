import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "~/components/ui/card";
import { Tracker } from "~/components/tracker/tracker";
import { type ExampleRun, type ExampleWithRuns, NUM_RUNS_PER_EXAMPLE } from "~/components/tracker/tracker-schema";

const nullData: ExampleRun[] = Array.from({ length: NUM_RUNS_PER_EXAMPLE }, (_, i) => ({
  id: i,
  background: "bg-slate-200",
}));

const nullExample: ExampleWithRuns = {
  id: 0,
  url: "Select an example to get started",
  runs: nullData,
}

interface Props {
  example?: ExampleWithRuns;
}
export function TrackerCard({ example }: Props) {
  const selectedExample = example ?? nullExample;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{selectedExample.url}</CardTitle>
        <CardDescription className="justify-between flex">
          <span>
            Statistics of the last 50 runs for this example
          </span>
          <span>0.0% Success</span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tracker data={selectedExample.runs}/>
      </CardContent>
    </Card>
  )
}
