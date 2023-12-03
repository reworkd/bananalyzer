import { db } from "~/server/db";
import { Card, Grid, Metric, Tab, TabGroup, TabList, TabPanel, TabPanels, Text, Title } from "@tremor/react";

export default async function Home() {
  // const hello = await api.post.hello.query({ text: "from tRPC" });
  // const session = await getServerAuthSession();

  return (
    <main className="min-h-screen p-10">
      <SuiteGrid />
      <Title className="font-medium text-2xl">Bananalytics 🍌</Title>
      <Text>Full stack Banalyses observability</Text>
      <TabGroup className="mt-6">
        <TabList>
          <Tab>Dashboard</Tab>
          <Tab>Runs</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Grid numItemsMd={2} numItemsLg={3} className="gap-6 mt-6">
              <Card>
                {/* Placeholder to set height */}
                <div className="h-28" />
              </Card>
              <Card>
                <Text>Tests run</Text>
                <Metric>10</Metric>
              </Card>
              <Card>
                {/* Placeholder to set height */}
                <div className="h-28" />
              </Card>
            </Grid>
            <div className="mt-6">
              <Card>
                <div className="h-80" />
              </Card>
            </div>
          </TabPanel>
          <TabPanel>
            <div className="mt-6">
              <Card>
                <div className="h-96" />
              </Card>
            </div>
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </main>
  );
}

async function SuiteGrid() {
  "use server";

  const suites = await db.testSuite.findMany();

  return (
    <>
      {/*<LineChart*/}
      {/*    className="mt-6"*/}
      {/*    data={chartdata}*/}
      {/*    index="year"*/}
      {/*    categories={["Export Growth Rate", "Import Growth Rate"]}*/}
      {/*    colors={["emerald", "gray"]}*/}
      {/*    // valueFormatter={valueFormatter}*/}
      {/*    yAxisWidth={40}*/}
      {/*/>*/}

      <div className="grid grid-cols-3">
        {suites.map((suite) => (
          <div key={suite.id}>
            <div>{suite.name}</div>
          </div>
        ))}
      </div>
    </>
  );
}
