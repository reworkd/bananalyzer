import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow, } from "~/components/ui/table"

const invoices = [
  {
    id: "INV001",
    status: "Paid",
    tags: "$250.00",
    paymentMethod: "Credit Card",
  },
  {
    id: "INV002",
    status: "Pending",
    tags: "$150.00",
    paymentMethod: "PayPal",
  },
  {
    id: "INV003",
    status: "Unpaid",
    tags: "$350.00",
    paymentMethod: "Bank Transfer",
  },
  {
    id: "INV004",
    status: "Paid",
    tags: "$450.00",
    paymentMethod: "Credit Card",
  },
  {
    id: "INV005",
    status: "Paid",
    tags: "$550.00",
    paymentMethod: "PayPal",
  },
  {
    id: "INV006",
    status: "Pending",
    tags: "$200.00",
    paymentMethod: "Bank Transfer",
  },
  {
    id: "INV007",
    status: "Unpaid",
    tags: "$300.00",
    paymentMethod: "Credit Card",
  },
]

export function ExampleTable() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]">Id</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Method</TableHead>
          <TableHead className="text-right">Amount</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {invoices.map((invoice) => (
          <TableRow key={invoice.id}>
            <TableCell className="font-medium">{invoice.id}</TableCell>
            <TableCell>{invoice.status}</TableCell>
            <TableCell>{invoice.paymentMethod}</TableCell>
            <TableCell className="text-right">{invoice.tags}</TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={3}>Perfect success percent</TableCell>
          <TableCell className="text-right">20%</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  )
}
