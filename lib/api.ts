import { getRuntimeConfig } from "./config";

export type AdminDropItem = {
  id: number;
  tenant_id: string;
  w3w_address: string | null;
  lat: number | null;
  lng: number | null;
  price_crypto: number | null;
  is_claimed: boolean;
  product_id: string | null;
};

export type AdminDropsResponse = {
  status: string;
  count: number;
  items: AdminDropItem[];
};

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function assertAdminDropsResponse(data: unknown): asserts data is AdminDropsResponse {
  if (!isObject(data)) {
    throw new Error("Invalid /admin/drops response: expected an object");
  }

  if (typeof data.status !== "string") {
    throw new Error("Invalid /admin/drops response: missing status");
  }

  if (typeof data.count !== "number") {
    throw new Error("Invalid /admin/drops response: missing count");
  }

  if (!Array.isArray(data.items)) {
    throw new Error("Invalid /admin/drops response: missing items array");
  }
}

export async function fetchAdminDrops(): Promise<AdminDropsResponse> {
  const { GFP_API_BASE_URL, GFP_ADMIN_API_KEY, GFP_TENANT_ID } = getRuntimeConfig();
  const url = `${GFP_API_BASE_URL.replace(/\/$/, "")}/admin/drops`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "X-API-Key": GFP_ADMIN_API_KEY,
      "X-Tenant-Id": GFP_TENANT_ID,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Failed to fetch admin drops (${response.status}): ${body || response.statusText}`);
  }

  const data: unknown = await response.json();
  assertAdminDropsResponse(data);
  return data;
}
