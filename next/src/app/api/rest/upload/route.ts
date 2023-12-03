import { createTRPCContext } from "~/server/api/trpc";
import { appRouter } from "~/server/api/root";
import { NextResponse } from "next/server";
import { parse, type TestSuites } from "junit2json";
import { TestSuiteSchema } from "~/schemas";
import { headers } from "next/headers";

export async function POST(req: Request) {
  const test_report = await req.text();

  let userToken = headers().get("Authorization");

  if (!userToken) {
    return NextResponse.json("Unauthorized", {
      status: 403,
    });
  }
  userToken = userToken.replace("Bearer ", "");

  const ctx = await createTRPCContext({
    headers: headers(),
  });

  const caller = appRouter.createCaller(ctx);
  const x = (await parse(test_report)) as TestSuites;

  const suite = x?.testsuite?.[0];
  if (!suite) {
    return;
  }

  const testSuite = {
    userId: userToken,
    name: suite.name,
    tests: suite.tests,
    failures: suite.failures,
    skipped: suite.skipped,
    errors: suite.errors,
    time: suite.time,
    timestamp: suite.timestamp,
    hostname: suite.hostname,
    testCases: (suite.testcase ?? []).map((testcase) => {
      return {
        name: testcase.name,
        classname: testcase.classname,
        time: testcase.time,
        status: "passed", // TODO: testcase.status,
        properties: ((testcase?.properties ?? []) as { name: string, value: string }[])
      });
    })
  }

  const result = await TestSuiteSchema.safeParseAsync(testSuite);
  if (!result.success) {
    return NextResponse.json(result.error, {
      status: 422,
    });
  }

  await caller.evaluations.create(result.data);
  return NextResponse.json("ok");
}
