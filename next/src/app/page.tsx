import { db } from "~/server/db";
import { Card, Grid, Metric, Tab, TabGroup, TabList, TabPanel, TabPanels, Text, Title } from "@tremor/react";
import TestSuitesTable from "~/app/_components/test-suites-table";
import TestSuiteChart from "~/app/_components/chart";

export default async function Home() {
  // const hello = await api.post.hello.query({ text: "from tRPC" });
  // const session = await getServerAuthSession();

  return (
    <main className="min-h-screen p-10">
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
              <NumTestsCard />
              <Card>
                {/* Placeholder to set height */}
                <div className="h-28" />
              </Card>
            </Grid>
            <div className="mt-6">
              <Card>
                <TestSuiteChart />
              </Card>
            </div>
          </TabPanel>
          <TabPanel>
            <div className="mt-6">
              <TestSuitesTable />
            </div>
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </main>
  );
}

async function NumTestsCard() {
  const numTests = await db.testSuite.count();

  return (
    <Card>
      <Text>Tests suites run</Text>
      <Metric>{numTests}</Metric>
    </Card>
  );
}
