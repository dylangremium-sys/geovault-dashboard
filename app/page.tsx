import { getAdminDrops, getAdminSummary, getHealth, getRoot } from "@/src/lib/api";
import type {
  AdminDropsResponse,
  AdminSummaryResponse,
  HealthResponse,
  RootResponse,
} from "@/src/types/api";

async function loadDashboardData(): Promise<{
  health?: HealthResponse;
  root?: RootResponse;
  summary?: AdminSummaryResponse;
  drops?: AdminDropsResponse;
  error?: string;
}> {
  try {
    const [health, root, summary, drops] = await Promise.all([
      getHealth(),
      getRoot(),
      getAdminSummary(),
      getAdminDrops(),
    ]);

    return { health, root, summary, drops };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

function Field({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="border border-neutral-800 bg-neutral-950 p-4">
      <div className="text-xs uppercase tracking-wide text-neutral-500">{label}</div>
      <div className="mt-2 text-2xl text-white">{value}</div>
    </div>
  );
}

export default async function Home() {
  const data = await loadDashboardData();

  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-8 border-b border-neutral-800 pb-6">
          <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">
            GeoVault Dashboard
          </div>
          <h1 className="mt-2 text-3xl font-semibold">Read-Only System Overview</h1>
          <p className="mt-3 max-w-2xl text-sm text-neutral-400">
            Minimal contract-aligned page using verified backend endpoints only.
          </p>
        </header>

        {data.error ? (
          <section className="border border-red-900 bg-red-950/30 p-4">
            <div className="text-xs uppercase tracking-wide text-red-400">Error</div>
            <div className="mt-2 text-sm text-red-200">{data.error}</div>
          </section>
        ) : (
          <>
            <section className="mb-8 grid gap-4 md:grid-cols-2">
              <div className="border border-neutral-800 bg-neutral-950 p-4">
                <div className="text-xs uppercase tracking-wide text-neutral-500">
                  API Health
                </div>
                <div className="mt-2 text-2xl text-white">
                  {data.health?.status ?? "Unavailable"}
                </div>
              </div>

              <div className="border border-neutral-800 bg-neutral-950 p-4">
                <div className="text-xs uppercase tracking-wide text-neutral-500">
                  API Message
                </div>
                <div className="mt-2 text-sm text-neutral-200">
                  {data.root?.message ?? "Unavailable"}
                </div>
              </div>
            </section>

            <section className="mb-8">
              <div className="mb-4 text-xs uppercase tracking-[0.2em] text-neutral-500">
                Admin Summary
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <Field
                  label="Total Drops"
                  value={data.summary?.summary.total_drops ?? "Unavailable"}
                />
                <Field
                  label="Claimed Drops"
                  value={data.summary?.summary.claimed_drops ?? "Unavailable"}
                />
                <Field
                  label="Total Entitlements"
                  value={data.summary?.summary.total_entitlements ?? "Unavailable"}
                />
                <Field
                  label="Used Entitlements"
                  value={data.summary?.summary.used_entitlements ?? "Unavailable"}
                />
              </div>
            </section>

            <section>
              <div className="mb-4 text-xs uppercase tracking-[0.2em] text-neutral-500">
                Admin Drops
              </div>

              <div className="overflow-x-auto border border-neutral-800 bg-neutral-950">
                <table className="min-w-full border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-neutral-800 text-left text-neutral-500">
                      <th className="px-4 py-3 font-medium">ID</th>
                      <th className="px-4 py-3 font-medium">W3W Address</th>
                      <th className="px-4 py-3 font-medium">Lat</th>
                      <th className="px-4 py-3 font-medium">Lng</th>
                      <th className="px-4 py-3 font-medium">Price Crypto</th>
                      <th className="px-4 py-3 font-medium">Claimed</th>
                      <th className="px-4 py-3 font-medium">Product ID</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.drops?.items.map((drop) => (
                      <tr key={drop.id} className="border-b border-neutral-900 align-top">
                        <td className="px-4 py-3 text-white">{drop.id}</td>
                        <td className="px-4 py-3 text-neutral-200">{drop.w3w_address}</td>
                        <td className="px-4 py-3 text-neutral-200">{drop.lat}</td>
                        <td className="px-4 py-3 text-neutral-200">{drop.lng}</td>
                        <td className="px-4 py-3 text-neutral-200">{drop.price_crypto}</td>
                        <td className="px-4 py-3 text-neutral-200">
                          {drop.is_claimed ? "true" : "false"}
                        </td>
                        <td className="px-4 py-3 text-neutral-200">
                          {drop.product_id ?? "null"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
