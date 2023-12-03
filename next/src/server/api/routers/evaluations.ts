import {z} from "zod";

import {createTRPCRouter, publicProcedure,} from "~/server/api/trpc";
import {TestSuiteSchema} from "~/schemas";



export const evalRouter = createTRPCRouter({
  create: publicProcedure
    .input(TestSuiteSchema)
    .mutation(async ({ input, ctx }) => {
      const suite = await ctx.db.testSuite.create({
        data: {
          name: input.name,
          tests: input.tests,
          failures: input.failures,
          skipped: input.skipped,
          errors: input.errors,
          time: input.time,
          hostname: input.hostname,
          createdById: "clpofluzg0000m7vjkmz7dxvv",
        }
      })

      for (const test of input.testCases) {
        const testCase = await ctx.db.testCase.create({
          data: {
            testSuiteId: suite.id,
            name: test.name,
            classname: test.classname,
            time: test.time,
            status: test.status,
            message: test.message,
          }
        })

        for (const property of test.properties) {
          await ctx.db.testCaseProperty.create({
            data: {
              testCaseId: testCase.id,
              name: property.name,
              value: property.value,
            }
          })
        }
      }


    // return suite
})});
