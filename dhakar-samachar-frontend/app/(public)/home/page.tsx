export default function HomePage() {
  return (
    <main className="mx-auto grid max-w-7xl gap-6 p-6 lg:grid-cols-4">
      <section className="lg:col-span-3 rounded bg-white p-6 shadow">
        <p className="text-sm font-semibold text-red-600">BREAKING</p>
        <h1 className="mt-2 text-3xl font-bold">Main headline section with configurable homepage blocks</h1>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <article className="rounded border p-4">Top news grid block</article>
          <article className="rounded border p-4">Category block news</article>
        </div>
      </section>
      <aside className="rounded bg-white p-6 shadow">Trending sidebar + ads area</aside>
    </main>
  );
}
