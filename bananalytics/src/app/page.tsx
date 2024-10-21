import { api, HydrateClient } from "~/trpc/server";
import { TrackerCard } from "~/components/tracker/tracker-card";
import { ExampleTableCard } from "~/components/example-table/example-table-card";
import { StatCard } from "~/components/stat-card";
import { ArrowRight } from "lucide-react";

export default async function Home() {
  const hello = await api.post.hello({ text: "from tRPC" });

  void api.post.getLatest.prefetch();

  return (
    <HydrateClient>
      <main className="flex min-h-screen justify-center">
        <div id="header" className="max-w-screen-xl w-full p-10">
          <div className="mb-10">

            <h1 className="text-4xl font-medium">Bananalytics 🍌</h1>
            <h3 className="text-md text-slate-500">Data extraction evaluations</h3>
          </div>

          <div id="content" className="flex flex-col gap-10">
            <div id="statistics" className="grid grid-cols-3 grid-rows-1 gap-2">
              <StatCard title="Number of examples" value="0" weeklyChange="+0" icon={<ArrowRight size={20}/>}/>
              <StatCard title="Number of examples" value="0" weeklyChange="+0" icon={<ArrowRight size={20}/>}/>
              <StatCard title="Number of examples" value="0" weeklyChange="+0" icon={<ArrowRight size={20}/>}/>
            </div>
            <ExampleTableCard />
            <TrackerCard />
          </div>
        </div>
      </main>
    </HydrateClient>
  );
}
