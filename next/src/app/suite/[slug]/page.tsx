import { Card, Col, Grid, Text, Title } from "@tremor/react";
import React from "react";

export default function Page({ params }: { params: { slug: string } }) {
  return (
    <main className="min-h-screen p-10">
      <Title className="text-2xl">Test suite <span className="font-bold">{params.slug}</span></Title>
      <Text>Fine grained analytics for test with id {params.slug}</Text>

      <Grid numItemsLg={6} className="gap-6 mt-6">
        {/* Main section */}
        <Col numColSpanLg={4}>
          <Card className="h-full">
            <div className="h-60" />
          </Card>
        </Col>

        {/* KPI sidebar */}
        <Col numColSpanLg={2}>
          <div className="space-y-6">
            <Card>
              <div className="h-24" />
            </Card>
            <Card>
              <div className="h-24" />
            </Card>
            <Card>
              <div className="h-24" />
            </Card>
          </div>
        </Col>
      </Grid>
    </main>
  )
}
