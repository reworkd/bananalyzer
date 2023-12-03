import { CreatePost } from "~/app/_components/create-post";
import { getServerAuthSession } from "~/server/auth";
import { api } from "~/trpc/server";
import {db} from "~/server/db";

export default async function Home() {
  // const hello = await api.post.hello.query({ text: "from tRPC" });
  // const session = await getServerAuthSession();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <h1>Bananalytics</h1>
      <SuiteGrid />
    </main>
  );
}

async function SuiteGrid() {
  "use server"


  const suites = await db.testSuite.findMany();

  return (
    <div className="grid grid-cols-2">
      {suites.map((suite) => (
        <div key={suite.id}>
          <div>{suite.name}</div>
        </div>
      ))}
    </div>
  );
}
