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
              <NumUsersCard />
              <NumTestsCard />
              <NumTestsSuitesCard />
            </Grid>
            <div className="mt-6">
              <TestSuiteChart />
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

async function NumUsersCard() {
  const numUsers = await db.user.count()

  return (
    <Card>
      <Text>Monkeys (Users)</Text>
      <Metric>{numUsers}</Metric>
    </Card>
  );
}

async function NumTestsSuitesCard() {
  const numTestSuites = await db.testSuite.count();

  return (
    <Card>
      <Text>Tests suites run</Text>
      <Metric>{numTestSuites}</Metric>
    </Card>
  );
}

async function NumTestsCard() {
  // Count an attribute of a model
  const testSuites = await db.testSuite.findMany()
  const numTests = testSuites.reduce((acc, curr) => acc + curr.tests, 0)

  return (
    <Card>
      <Text>Tests tests run</Text>
      <Metric>{numTests}</Metric>
    </Card>
  );
}
