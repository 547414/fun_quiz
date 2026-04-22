"use client";

import type { ReactNode } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableHead, TableHeader, TableRow } from "@/components/ui/table";

type DataListPanelProps = {
  title: string;
  actions?: ReactNode;
  filters?: ReactNode;
  headers: string[];
  children: ReactNode;
  emptyState?: ReactNode;
};

export function DataListPanel({ title, actions, filters, headers, children, emptyState }: DataListPanelProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-4">
        <CardTitle className="text-xl">{title}</CardTitle>
        {actions}
      </CardHeader>
      <CardContent className="space-y-4">
        {filters}
        <div className="overflow-hidden rounded-xl border border-border">
          <Table>
            <TableHeader>
              <TableRow>
                {headers.map((header) => (
                  <TableHead key={header}>{header}</TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>{children}</TableBody>
          </Table>
        </div>
        {emptyState}
      </CardContent>
    </Card>
  );
}
