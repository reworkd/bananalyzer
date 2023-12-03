import { AreaChart, Card, Title } from "@tremor/react";
import { db } from "~/server/db";

export default async function() {
  const testSuites = await db.testSuite.findMany();
  const data = testSuites.map((t) => ({
    date: new Date(t.createdAt).toLocaleDateString(),
    "Failures": t.failures,
    "Errors": t.errors,
    "Successes": t.tests - t.failures - t.errors,
  }));

  return (
    <Card>
      <Title>Bananalyses over time</Title>
      <AreaChart
        className="h-72 mt-4"
        data={data}
        index="date"
        categories={["Successes", "Failures", "Errors"]}
        colors={["green", "red", "rose"]}
      />
    </Card>
  );
}
