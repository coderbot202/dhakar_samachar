import Link from 'next/link';

const sections = [
  { href: '/home', label: 'Public Homepage' },
  { href: '/dashboard', label: 'Admin Dashboard' },
  { href: '/login', label: 'Authentication' },
];

export default function LandingPage() {
  return (
    <main className="mx-auto max-w-5xl p-8">
      <h1 className="text-4xl font-bold text-red-700">Dhakar Samachar Platform</h1>
      <p className="mt-3 text-slate-700">Next.js 14 App Router scaffold inspired by Dainik Bhaskar style blocks.</p>
      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        {sections.map((section) => (
          <Link key={section.href} href={section.href} className="rounded border bg-white p-4 shadow-sm hover:border-red-500">
            {section.label}
          </Link>
        ))}
      </div>
    </main>
  );
}
