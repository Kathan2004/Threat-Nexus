"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { CheckCircle2, KeyRound, Save, ShieldAlert, ToggleLeft, ToggleRight } from "lucide-react";

type SourceConfig = {
  id: string;
  display_name: string;
  enabled: boolean;
  base_url: string | null;
  required_credentials: string[];
  configured_credentials: string[];
  missing_credentials: string[];
  updated_at: string | null;
  updated_by: string | null;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function SettingsPage() {
  const [token, setToken] = useState("");
  const [sources, setSources] = useState<SourceConfig[]>([]);
  const [selected, setSelected] = useState<SourceConfig | null>(null);
  const [enabled, setEnabled] = useState(false);
  const [baseUrl, setBaseUrl] = useState("");
  const [credentials, setCredentials] = useState<Record<string, string>>({});
  const [status, setStatus] = useState("Enter an API bearer token to load source settings.");

  const configuredCount = useMemo(
    () => sources.filter((source) => source.enabled && source.missing_credentials.length === 0).length,
    [sources],
  );

  async function loadSources() {
    if (!token) {
      setStatus("Bearer token is required.");
      return;
    }
    const response = await fetch(`${apiBaseUrl}/settings/sources`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
      setStatus(`Unable to load settings: ${response.status}`);
      return;
    }
    const data = (await response.json()) as SourceConfig[];
    setSources(data);
    setSelected(data[0] ?? null);
    setStatus("Source settings loaded.");
  }

  useEffect(() => {
    if (!selected) {
      return;
    }
    setEnabled(selected.enabled);
    setBaseUrl(selected.base_url ?? "");
    setCredentials({});
  }, [selected]);

  async function saveSource(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selected) {
      return;
    }
    const response = await fetch(`${apiBaseUrl}/settings/sources/${selected.id}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        enabled,
        base_url: baseUrl,
        credentials,
      }),
    });
    if (!response.ok) {
      setStatus(`Save failed: ${response.status}`);
      return;
    }
    const updated = (await response.json()) as SourceConfig;
    setSources((current) => current.map((source) => (source.id === updated.id ? updated : source)));
    setSelected(updated);
    setCredentials({});
    setStatus(`${updated.display_name} saved.`);
  }

  return (
    <main className="min-h-screen bg-background text-slate-100">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-border bg-panel px-4 py-5 lg:block">
        <a href="/" className="mb-7 flex items-center gap-3 text-lg font-semibold">
          <ShieldAlert className="h-6 w-6 text-accent" />
          Threat Nexus
        </a>
        <nav className="space-y-1">
          <a href="/" className="block rounded-md px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">
            Dashboard
          </a>
          <a href="/settings" className="block rounded-md bg-slate-800 px-3 py-2 text-sm text-white">
            Settings
          </a>
        </nav>
      </aside>

      <section className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-border bg-background/90 px-5 py-4 backdrop-blur">
          <h1 className="text-xl font-semibold">Source Configuration</h1>
          <p className="text-sm text-slate-400">Enable intelligence sources and store plugin credentials through the backend settings API.</p>
        </header>

        <div className="grid gap-5 p-5 xl:grid-cols-[340px_1fr]">
          <section className="rounded-lg border border-border bg-panel">
            <div className="border-b border-border p-4">
              <label className="text-sm text-slate-300" htmlFor="token">
                API bearer token
              </label>
              <div className="mt-2 flex gap-2">
                <input
                  id="token"
                  type="password"
                  value={token}
                  onChange={(event) => setToken(event.target.value)}
                  className="min-w-0 flex-1 rounded-md border border-border bg-slate-950 px-3 py-2 text-sm outline-none focus:border-accent"
                  placeholder="Paste token"
                />
                <button type="button" onClick={loadSources} className="rounded-md bg-accent px-3 py-2 text-sm font-medium text-slate-950">
                  Load
                </button>
              </div>
              <p className="mt-3 text-xs text-slate-400">{status}</p>
            </div>

            <div className="border-b border-border p-4">
              <p className="text-sm text-slate-400">Ready sources</p>
              <p className="mt-1 text-3xl font-semibold">{configuredCount}</p>
            </div>

            <div className="max-h-[calc(100vh-260px)] overflow-auto">
              {sources.map((source) => (
                <button
                  key={source.id}
                  type="button"
                  onClick={() => setSelected(source)}
                  className={`flex w-full items-center justify-between border-b border-border px-4 py-3 text-left text-sm ${
                    selected?.id === source.id ? "bg-slate-800 text-white" : "text-slate-300 hover:bg-slate-900"
                  }`}
                >
                  <span>{source.display_name}</span>
                  {source.enabled ? <ToggleRight className="h-5 w-5 text-accent" /> : <ToggleLeft className="h-5 w-5 text-slate-500" />}
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-border bg-panel p-5">
            {selected ? (
              <form onSubmit={saveSource} className="space-y-5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h2 className="text-lg font-semibold">{selected.display_name}</h2>
                    <p className="text-sm text-slate-400">{selected.id}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setEnabled((value) => !value)}
                    className="flex items-center gap-2 rounded-md border border-border px-3 py-2 text-sm text-slate-200"
                  >
                    {enabled ? <ToggleRight className="h-5 w-5 text-accent" /> : <ToggleLeft className="h-5 w-5 text-slate-500" />}
                    {enabled ? "Enabled" : "Disabled"}
                  </button>
                </div>

                <label className="block text-sm text-slate-300" htmlFor="base-url">
                  Base URL
                  <input
                    id="base-url"
                    type="url"
                    value={baseUrl}
                    onChange={(event) => setBaseUrl(event.target.value)}
                    className="mt-2 w-full rounded-md border border-border bg-slate-950 px-3 py-2 text-sm outline-none focus:border-accent"
                    placeholder="https://api.example.com"
                  />
                </label>

                <div>
                  <div className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-200">
                    <KeyRound className="h-4 w-4 text-accent" />
                    Credentials
                  </div>
                  <div className="grid gap-3 md:grid-cols-2">
                    {selected.required_credentials.length ? (
                      selected.required_credentials.map((name) => (
                        <label key={name} className="block text-sm text-slate-300">
                          {name}
                          <input
                            type="password"
                            value={credentials[name] ?? ""}
                            onChange={(event) => setCredentials((current) => ({ ...current, [name]: event.target.value }))}
                            className="mt-2 w-full rounded-md border border-border bg-slate-950 px-3 py-2 text-sm outline-none focus:border-accent"
                            placeholder={selected.configured_credentials.includes(name) ? "Already configured" : "Required"}
                          />
                        </label>
                      ))
                    ) : (
                      <p className="text-sm text-slate-400">This source does not require credentials.</p>
                    )}
                  </div>
                </div>

                <div className="rounded-md border border-border bg-slate-950 p-4 text-sm text-slate-300">
                  <div className="mb-2 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-accent" />
                    Configured credential names
                  </div>
                  <p>{selected.configured_credentials.length ? selected.configured_credentials.join(", ") : "None yet"}</p>
                  <p className="mt-2 text-slate-500">Secret values are never returned to the frontend after saving.</p>
                </div>

                <button type="submit" className="inline-flex items-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-semibold text-slate-950">
                  <Save className="h-4 w-4" />
                  Save source
                </button>
              </form>
            ) : (
              <div className="grid min-h-96 place-items-center text-sm text-slate-400">Load settings to edit source credentials.</div>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}
