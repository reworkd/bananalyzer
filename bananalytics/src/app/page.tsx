import { api, HydrateClient } from "~/trpc/server";
import { TrackerCard } from "~/components/tracker/tracker-card";
import { ExampleTableCard } from "~/components/example-table/example-table-card";

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

          <div id="content" className="flex flex-col gap-4">
            <TrackerCard />
            <ExampleTableCard />
          </div>
        </div>
      </main>
    </HydrateClient>
  );
}
