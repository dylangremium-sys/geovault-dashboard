import Panel from "@/src/components/ui/Panel";
import {
  getAdminDrops,
  getAdminEntitlements,
  getAdminSummary,
  getHealth,
  getRoot,
  postCreateDrop,
} from "@/src/lib/api";
import type {
  AdminDropsResponse,
  AdminEntitlementsResponse,
  AdminSummaryResponse,
  CreateDropSuccessResponse,
  HealthResponse,
  RootResponse,
} from "@/src/types/api";

type DashboardData = {
  health?: HealthResponse;
  root?: RootResponse;
  summary?: AdminSummaryResponse;
  drops?: AdminDropsResponse;
  entitlements?: AdminEntitlementsResponse;
  error?: string;
};

async function loadDashboardData(): Promise<DashboardData> {
  try {
    const [health, root, summary, drops, entitlements] = await Promise.all([
      getHealth(),
      getRoot(),
      getAdminSummary(),
      getAdminDrops(),
      getAdminEntitlements(),
    ]);

    return { health, root, summary, drops, entitlements };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

async function createDropAction(formData: FormData): Promise<void> {
  "use server";

  await postCreateDrop({
    w3w_address: String(formData.get("w3w_address") ?? ""),
    lat: Number(formData.get("lat")),
    lng: Number(formData.get("lng")),
    price_crypto: Number(formData.get("price_crypto")),
  });
}

function SectionTitle({ children }: { children: string }) {
  return (
    <div className="mb-4 text-xs uppercase tracking-[0.2em] text-neutral-500">
      {children}
    </div>
  );
}
function Field({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <Panel label={label}>
      <div className="text-2xl text-white">{value}</div>
    </Panel>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <section className="border border-red-900 bg-red-950/30 p-4">
      <div className="text-xs uppercase tracking-wide text-red-400">Error</div>
      <div className="mt-2 text-sm text-red-200">{message}</div>
    </section>
  );
}

function KeyValueOverview({
  health,
  root,
}: {
  health?: HealthResponse;
  root?: RootResponse;
}) {
  return (
    <section className="mb-8 grid gap-4 md:grid-cols-2">
      <Panel label="API Health">
        <div className="text-2xl text-white">{health?.status ?? "Unavailable"}</div>
      </Panel>

      <Panel label="API Message">
        <div className="text-sm text-neutral-200">
          {root?.message ?? "Unavailable"}
        </div>
      </Panel>
    </section>
  );
}

function SummarySection({ summary }: { summary?: AdminSummaryResponse }) {
  return (
    <section className="mb-8">
      <SectionTitle>Admin Summary</SectionTitle>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Field
          label="Total Drops"
          value={summary?.summary.total_drops ?? "Unavailable"}
        />
        <Field
          label="Claimed Drops"
          value={summary?.summary.claimed_drops ?? "Unavailable"}
        />
        <Field
          label="Total Entitlements"
          value={summary?.summary.total_entitlements ?? "Unavailable"}
        />
        <Field
          label="Used Entitlements"
          value={summary?.summary.used_entitlements ?? "Unavailable"}
        />
      </div>
    </section>
  );
}

function DataTable({
  headers,
  rows,
}: {
  headers: string[];
  rows: React.ReactNode;
}) {
  return (
    <div className="overflow-x-auto border border-neutral-800 bg-neutral-950">
      <table className="min-w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-neutral-800 text-left text-neutral-500">
            {headers.map((header) => (
              <th key={header} className="px-4 py-3 font-medium">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  );
}

function DropsSection({ drops }: { drops?: AdminDropsResponse }) {
  return (
    <section className="mb-8">
      <SectionTitle>Admin Drops</SectionTitle>

      <DataTable
        headers={[
          "ID",
          "W3W Address",
          "Lat",
          "Lng",
          "Price Crypto",
          "Claimed",
          "Product ID",
        ]}
        rows={drops?.items.map((drop) => (
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
      />
    </section>
  );
}

function EntitlementsSection({
  entitlements,
}: {
  entitlements?: AdminEntitlementsResponse;
}) {
  return (
    <section className="mb-8">
      <SectionTitle>Admin Entitlements</SectionTitle>

      <DataTable
        headers={[
          "ID",
          "Drop ID",
          "Payment ID",
          "Used",
          "Expires At",
          "Created At",
        ]}
        rows={entitlements?.items.map((entitlement) => (
          <tr
            key={entitlement.id}
            className="border-b border-neutral-900 align-top"
          >
            <td className="px-4 py-3 text-white">{entitlement.id}</td>
            <td className="px-4 py-3 text-neutral-200">{entitlement.drop_id}</td>
            <td className="px-4 py-3 text-neutral-200">
              {entitlement.payment_id}
            </td>
            <td className="px-4 py-3 text-neutral-200">
              {entitlement.is_used ? "true" : "false"}
            </td>
            <td className="px-4 py-3 text-neutral-200">
              {entitlement.expires_at ?? "null"}
            </td>
            <td className="px-4 py-3 text-neutral-200">
              {entitlement.created_at ?? "null"}
            </td>
          </tr>
        ))}
      />
    </section>
  );
}

function CreateDropSection() {
  return (
    <section>
      <SectionTitle>Create Drop</SectionTitle>

      <form action={createDropAction} className="grid max-w-md gap-3">
        <input
          name="w3w_address"
          placeholder="w3w_address"
          className="border border-neutral-800 bg-black p-2 text-white"
          required
        />
        <input
          name="lat"
          placeholder="lat"
          className="border border-neutral-800 bg-black p-2 text-white"
          required
        />
        <input
          name="lng"
          placeholder="lng"
          className="border border-neutral-800 bg-black p-2 text-white"
          required
        />
        <input
          name="price_crypto"
          placeholder="price_crypto"
          className="border border-neutral-800 bg-black p-2 text-white"
          required
        />
        <button type="submit" className="bg-white p-2 text-black">
          Submit
        </button>
      </form>
    </section>
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
          <ErrorState message={data.error} />
        ) : (
          <>
            <KeyValueOverview health={data.health} root={data.root} />
            <SummarySection summary={data.summary} />
            <DropsSection drops={data.drops} />
            <EntitlementsSection entitlements={data.entitlements} />
            <CreateDropSection />
          </>
        )}
      </div>
    </main>
  );
}
