"use server";
import { type TestSuite } from "@prisma/client";
import { db } from "~/server/db";
import {
  Badge,
  Button,
  Card,
  Flex,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeaderCell,
  TableRow,
  Text,
  Title
} from "@tremor/react";

export default async function TestSuitesTable() {
  const suites: TestSuite[] = await db.testSuite.findMany();

  return (
    <Card>
      <Flex justifyContent="start" className="space-x-2">
        <Title>Test Suite Runs</Title>
        <Badge color="gray">{suites.length}</Badge>
      </Flex>
      <Text className="mt-2">Overview of this month's purchases</Text>
      <Table className="mt-6">
        <TableHead>
          <TableRow>
            <TableHeaderCell>Test ID</TableHeaderCell>
            <TableHeaderCell>Create date</TableHeaderCell>
            <TableHeaderCell>Tests Run (#)</TableHeaderCell>
            <TableHeaderCell>Successes (#)</TableHeaderCell>
            <TableHeaderCell>Failures (#)</TableHeaderCell>
            <TableHeaderCell>Errors (#)</TableHeaderCell>
            <TableHeaderCell>Link</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {suites.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.id}</TableCell>
              <TableCell>{new Date(item.createdAt).toLocaleString()}</TableCell>
              <TableCell>{item.tests}</TableCell>
              <TableCell>{item.tests - item.errors - item.failures}</TableCell>
              <TableCell>
                {item.failures}
              </TableCell>
              <TableCell>
                {item.errors}
              </TableCell>
              <TableCell>
                <Button size="xs" color="neutral">
                  See details
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}
