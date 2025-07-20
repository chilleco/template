import { Suspense } from "react";
import UsersPreview from "./users/_users-preview";

export const metadata = { title: "Dashboard – overview" };

export default async function DashboardHome() {
  return (
    <>
      <h1 className="mb-6 text-3xl font-bold">Overview</h1>

      <Suspense fallback={<p>Loading users…</p>}>
        {/* RSC, фечится на сервере */}
        <UsersPreview limit={5} />
      </Suspense>
    </>
  );
}
