"use client";

import { useEffect } from "react";

import { Button } from "@/components/ui/button";
import { useBootstrapSession } from "@/features/users/api";

export default function UsersView() {
  const { mutate, data, isPending } = useBootstrapSession();

  useEffect(() => {
    mutate();
  }, [mutate]);

  return (
    <div className="rounded-lg border p-6">
      <h2 className="text-xl font-semibold">User session bootstrap</h2>
      <p className="mt-2 text-sm text-muted-foreground">
        Pre-auth tokens preserve cart/favorites before a user signs in.
      </p>
      <Button className="mt-4" disabled={isPending} onClick={() => mutate()}>
        {isPending ? "Issuing…" : "Re-issue token"}
      </Button>
      {data ? (
        <pre className="mt-4 overflow-x-auto rounded bg-muted p-4 text-sm">{JSON.stringify(data, null, 2)}</pre>
      ) : null}
    </div>
  );
}
