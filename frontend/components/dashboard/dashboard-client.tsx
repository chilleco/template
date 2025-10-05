'use client';

import { useEffect, useState } from 'react';

import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface Metric {
  label: string;
  value: string;
}

const baseMetrics: Metric[] = [
  { label: 'Background queue latency', value: '42 ms' },
  { label: 'Websocket subscribers', value: '128' },
  { label: 'AI-generated commits awaiting review', value: '3' }
];

export function DashboardClient() {
  const [metrics, setMetrics] = useState<Metric[]>(baseMetrics);

  useEffect(() => {
    const listener = () => setMetrics(current => [...current]);
    document.addEventListener('auth:unauthorized', listener);
    return () => document.removeEventListener('auth:unauthorized', listener);
  }, []);

  return (
    <div className="mt-8 grid gap-6 md:grid-cols-3">
      {metrics.map(metric => (
        <Card key={metric.label}>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-foreground/60">{metric.label}</CardTitle>
            <CardDescription className="text-2xl font-semibold text-foreground">{metric.value}</CardDescription>
          </CardHeader>
        </Card>
      ))}
    </div>
  );
}
