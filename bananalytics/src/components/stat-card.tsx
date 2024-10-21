import { Card, CardContent } from "~/components/ui/card";
import { type ReactNode } from "react";

interface Props {
  title: string;
  value: string
  icon?: ReactNode;
  weeklyChange?: string;
}

export function StatCard({ title, value, icon, weeklyChange }: Props) {
  return (
    <Card>
      <CardContent className="pt-6 flex flex-col gap-2">
        <div className="flex w-full justify-between items-center">
          <h3 className="text-xs text-slate-500">{title}</h3>
          {icon}
        </div>

        <div>

          <div className="flex items-end gap-2">
            <span className="font-medium text-3xl">
              {value}
            </span>
            <span className="text-sm pb-1 text-slate-500">
              {weeklyChange}%
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
