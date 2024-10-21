import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "~/components/ui/card";
import { ExampleTable } from "~/components/example-table/example-table";


export function ExampleTableCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Examples</CardTitle>
        <CardDescription>
          An overview of all available examples
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ExampleTable />
      </CardContent>
    </Card>
  )
}
