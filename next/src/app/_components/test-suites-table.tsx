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
  Title,
} from "@tremor/react";
import { db } from "~/server/db";

const colors = {
  "Ready for dispatch": "gray",
  Cancelled: "rose",
  Shipped: "emerald",
};

const transactions = [
  {
    transactionID: "#123456",
    user: "Lena Mayer",
    item: "Under Armour Shorts",
    status: "Ready for dispatch",
    amount: "$ 49.90",
    link: "#",
  },
  {
    transactionID: "#234567",
    user: "Max Smith",
    item: "Book - Wealth of Nations",
    status: "Ready for dispatch",
    amount: "$ 19.90",
    link: "#",
  },
  {
    transactionID: "#345678",
    user: "Anna Stone",
    item: "Garmin Forerunner 945",
    status: "Cancelled",
    amount: "$ 499.90",
    link: "#",
  },
  {
    transactionID: "#4567890",
    user: "Truls Cumbersome",
    item: "Running Backpack",
    status: "Shipped",
    amount: "$ 89.90",
    link: "#",
  },
  {
    transactionID: "#5678901",
    user: "Peter Pikser",
    item: "Rolex Submariner Replica",
    status: "Cancelled",
    amount: "$ 299.90",
    link: "#",
  },
  {
    transactionID: "#6789012",
    user: "Phlipp Forest",
    item: "On Clouds Shoes",
    status: "Ready for dispatch",
    amount: "$ 290.90",
    link: "#",
  },
  {
    transactionID: "#78901234",
    user: "Mara Pacemaker",
    item: "Ortovox Backpack 40l",
    status: "Shipped",
    amount: "$ 150.00",
    link: "#",
  },
  {
    transactionID: "#89012345",
    user: "Sev Major",
    item: "Oakley Jawbreaker",
    status: "Ready for dispatch",
    amount: "$ 190.90",
    link: "#",
  },
];

export default async function TestSuitesTable() {
  "use server";
  const suites = await db.testSuite.findMany();

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
