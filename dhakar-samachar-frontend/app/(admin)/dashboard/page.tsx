export default function AdminDashboardPage() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      <div className="mt-4 grid gap-4 md:grid-cols-3">
        <div className="rounded bg-white p-4 shadow">Article statistics</div>
        <div className="rounded bg-white p-4 shadow">Trending articles</div>
        <div className="rounded bg-white p-4 shadow">Traffic charts</div>
      </div>
    </main>
  );
}
