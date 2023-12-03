import {type NextApiRequest} from "next";
import {createTRPCContext} from "~/server/api/trpc";
import {appRouter} from "~/server/api/root";
import {NextResponse} from "next/server";
import {parse, TestSuites} from 'junit2json'
import fs from 'fs/promises';
import {TestSuiteSchema} from "~/schemas";

const PATH
  = '/Users/awtkns/PycharmProjects/bananalyzer/.banana_cache/tmpha02dk07_report.html';

const handler = async (req: NextApiRequest) => {

  const xmlData = await fs.readFile(PATH, 'utf8');



  // Create context and caller
  const headers = Object.entries(req.headers).reduce((acc, [key, value]) => {
  if (typeof value === "string") {
    acc.append(key, value);
  }
  return acc;
}, new Headers());

  const ctx = await createTRPCContext({
    headers: headers,
  });

  const caller = appRouter.createCaller(ctx);
  const x = await parse(xmlData) as TestSuites;

  const suite = x?.testsuite?.[0];
  if (!suite) {
    return
  }

  const testSuite = {
    name: suite.name,
    tests: suite.tests,
    failures: suite.failures,
    skipped: suite.skipped,
    errors: suite.errors,
    time: suite.time,
    timestamp: suite.timestamp,
    hostname: suite.hostname,
    testCases: (suite.testcase ?? []).map(testcase => {
      return ({
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
      status: 422
    });

  }

  await caller.evaluations.create(result.data)
  return NextResponse.json("ok");
};

export { handler as GET };
