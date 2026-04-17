import { fetchAdminDrops } from "../../../lib/api";

export default async function AdminDropsPage() {
  const data = await fetchAdminDrops();

  return (
    <main style={{ padding: "24px", fontFamily: "sans-serif" }}>
      <h1 style={{ marginBottom: "8px" }}>Drops List</h1>
      <p style={{ marginBottom: "16px" }}>Count: {data.count}</p>

      {data.items.length === 0 ? (
        <p>No drops found.</p>
      ) : (
        <div style={{ overflowX: "auto" }}>
          <table style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>id</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>tenant_id</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>w3w_address</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>lat</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>lng</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>price_crypto</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>is_claimed</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>product_id</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((item) => (
                <tr key={item.id}>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.id}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.tenant_id}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.w3w_address ?? ""}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.lat ?? ""}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.lng ?? ""}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.price_crypto ?? ""}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{String(item.is_claimed)}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{item.product_id ?? ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
