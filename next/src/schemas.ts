import {z} from "zod";

export const TestCaseSchema = z.object({
  name: z.string(),
  classname: z.string().optional(),
  time: z.number(),
  status: z.enum(["passed", "failed", "skipped"]),
  message: z.string().optional(),
  properties: z.array(z.object({
    name: z.string(),
    value: z.string()
  }))
});

export const TestSuiteSchema = z.object({
  name: z.string(),
  testCases: z.array(TestCaseSchema),
  tests: z.number().int().gte(0),
  failures: z.number().int().gte(0),
  skipped: z.number(),
  errors: z.number().int().gte(0),
  time: z.number().gte(0),
  hostname: z.string(),
});


export type TestCase = z.infer<typeof TestCaseSchema>;
export type TestSuite = z.infer<typeof TestSuiteSchema>;
