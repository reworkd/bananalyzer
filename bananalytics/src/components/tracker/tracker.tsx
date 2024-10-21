import { cn } from "~/lib/utils";
import { type ExampleRun } from "~/components/tracker/tracker-schema";

interface TrackerProps {
  data: ExampleRun[];
}

export function Tracker({ data }: TrackerProps) {
  return <div className="w-full flex flex-col gap-2">
    <TrackerBar data={data} />
    <div className="w-full justify-between flex text-slate-500 text-xs">
      <div>Oldest</div>
      <div>Newest</div>
    </div>
  </div>;
}

function TrackerBar({ data }: TrackerProps) {
  return <div className="flex gap-1 w-full first:rounded-xl">
    {data.map((exampleTracker) => (
      <div key={exampleTracker.id}
           className={cn(exampleTracker.background, "flex-grow h-10 bg-slate-100 first:rounded-l-md last:rounded-r-md")} />
    ))}
  </div>;
}
