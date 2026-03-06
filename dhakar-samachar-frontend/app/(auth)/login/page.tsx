export default function LoginPage() {
  return (
    <main className="mx-auto max-w-md p-6">
      <h1 className="text-2xl font-bold">Login</h1>
      <form className="mt-4 space-y-3 rounded bg-white p-4 shadow">
        <input className="w-full rounded border p-2" placeholder="Email" />
        <input className="w-full rounded border p-2" placeholder="Password" type="password" />
        <button className="w-full rounded bg-red-600 p-2 text-white" type="submit">Sign in</button>
      </form>
    </main>
  );
}
