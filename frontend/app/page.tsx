import { Activity, AlertTriangle, Database, Network, Search, ShieldAlert } from "lucide-react";

const nav = ["Dashboard", "Threat Feed", "Threat Actors", "Campaigns", "Malware", "CVEs", "IOCs", "Alerts", "Analytics", "Settings"];
const metrics = [
  ["Critical Alerts", "18", "Active response required"],
  ["Tracked CVEs", "1,284", "71 in KEV"],
  ["Observed IOCs", "92k", "Last 24h ingestion"],
  ["Confidence Avg", "86%", "Across enriched intel"],
];
const feed = [
  ["CRITICAL", "Mass exploitation observed for edge appliance CVE", "CISA KEV, GreyNoise, Shodan"],
  ["HIGH", "Ransomware affiliate infrastructure rotates domains", "Ransomware.live, URLHaus"],
  ["MEDIUM", "APT cluster reuses loader in regional campaign", "MISP, OpenCTI"],
];

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-border bg-panel px-4 py-5 lg:block">
        <div className="mb-7 flex items-center gap-3 text-lg font-semibold">
          <ShieldAlert className="h-6 w-6 text-accent" />
          Threat Nexus
        </div>
        <nav className="space-y-1">
          {nav.map((item) => (
            <a key={item} href={item === "Settings" ? "/settings" : "/"} className="block w-full rounded-md px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-white">
              {item}
            </a>
          ))}
        </nav>
      </aside>
      <section className="lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-border bg-background/90 px-5 backdrop-blur">
          <div>
            <h1 className="text-xl font-semibold">Threat Operations Dashboard</h1>
            <p className="text-xs text-slate-400">Continuous intelligence aggregation, enrichment, and distribution</p>
          </div>
          <div className="flex items-center gap-2 rounded-md border border-border bg-panel px-3 py-2 text-sm text-slate-300">
            <Search className="h-4 w-4" />
            Search intelligence
          </div>
        </header>
        <div className="grid gap-4 p-5 xl:grid-cols-4">
          {metrics.map(([label, value, hint]) => (
            <div key={label} className="rounded-lg border border-border bg-panel p-4">
              <p className="text-sm text-slate-400">{label}</p>
              <p className="mt-2 text-3xl font-semibold">{value}</p>
              <p className="mt-2 text-xs text-slate-500">{hint}</p>
            </div>
          ))}
        </div>
        <div className="grid gap-5 p-5 pt-0 xl:grid-cols-[1.4fr_1fr]">
          <section className="rounded-lg border border-border bg-panel">
            <div className="flex items-center gap-2 border-b border-border p-4">
              <Activity className="h-5 w-5 text-accent" />
              <h2 className="font-semibold">Enriched Threat Feed</h2>
            </div>
            <div className="divide-y divide-border">
              {feed.map(([severity, title, sources]) => (
                <article key={title} className="grid gap-3 p-4 md:grid-cols-[120px_1fr]">
                  <span className={severity === "CRITICAL" ? "text-sm font-semibold text-danger" : "text-sm font-semibold text-accent"}>{severity}</span>
                  <div>
                    <h3 className="font-medium">{title}</h3>
                    <p className="mt-1 text-sm text-slate-400">{sources}</p>
                  </div>
                </article>
              ))}
            </div>
          </section>
          <section className="rounded-lg border border-border bg-panel p-4">
            <div className="mb-4 flex items-center gap-2">
              <Network className="h-5 w-5 text-accent" />
              <h2 className="font-semibold">Correlation Graph</h2>
            </div>
            <div className="grid aspect-square place-items-center rounded-md border border-border bg-slate-950">
              <div className="grid grid-cols-2 gap-6 text-center text-sm text-slate-300">
                <span><AlertTriangle className="mx-auto mb-2 h-7 w-7 text-danger" />Alerts</span>
                <span><Database className="mx-auto mb-2 h-7 w-7 text-accent" />Sources</span>
                <span>Actors</span>
                <span>Malware</span>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
