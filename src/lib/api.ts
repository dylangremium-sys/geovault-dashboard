import { API_BASE_URL, ADMIN_API_KEY, TENANT_ID } from "./config";
import type {
  AdminDropsResponse,
  AdminEntitlementsResponse,
  AdminSummaryResponse,
  ClaimRequest,
  ClaimResponse,
  CreateDropRequest,
  CreateDropSuccessResponse,
  CreatePaymentRequest,
  CreatePaymentSuccessResponse,
  HealthResponse,
  PaymentsCallbackResponse,
  RevealRequest,
  RevealSuccessResponse,
  RootResponse,
  NearbyDropListItem,
} from "@/src/types/api";

type RequestOptions = {
  method?: "GET" | "POST";
  headers?: Record<string, string>;
  body?: string;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      ...(options.headers ?? {}),
    },
    body: options.body,
    cache: "no-store",
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Unauthorized. Check dashboard API key.");
    }
    if (response.status === 422) {
      throw new Error("Request validation failed.");
    }
    if (response.status >= 500) {
      throw new Error("Backend unavailable.");
    }
    throw new Error(`Request failed (${response.status})`);
  }

  return response.json() as Promise<T>;
}

function adminHeaders(): Record<string, string> {
  return {
    ...(ADMIN_API_KEY ? { "x-api-key": ADMIN_API_KEY } : {}),
    ...(TENANT_ID ? { "X-Tenant-Id": TENANT_ID } : {}),
  };
}

export async function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export async function getRoot(): Promise<RootResponse> {
  return request<RootResponse>("/");
}

export async function getNearbyDrops(params: {
  lat: number;
  lng: number;
  radius_km?: number;
}): Promise<NearbyDropListItem[]> {
  const search = new URLSearchParams({
    lat: String(params.lat),
    lng: String(params.lng),
    radius_km: String(params.radius_km ?? 10),
  });

  return request<NearbyDropListItem[]>(`/drops/nearby?${search.toString()}`);
}

export async function getAdminDrops(): Promise<AdminDropsResponse> {
  return request<AdminDropsResponse>("/admin/drops", {
    headers: adminHeaders(),
  });
}

export async function getAdminEntitlements(): Promise<AdminEntitlementsResponse> {
  return request<AdminEntitlementsResponse>("/admin/entitlements", {
    headers: adminHeaders(),
  });
}

export async function getAdminSummary(): Promise<AdminSummaryResponse> {
  return request<AdminSummaryResponse>("/admin/summary", {
    headers: adminHeaders(),
  });
}

export async function postClaim(payload: ClaimRequest): Promise<ClaimResponse> {
  return request<ClaimResponse>("/claim", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function postReveal(
  payload: RevealRequest,
): Promise<RevealSuccessResponse> {
  return request<RevealSuccessResponse>("/reveal", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function postCreatePayment(
  payload: CreatePaymentRequest,
): Promise<CreatePaymentSuccessResponse> {
  return request<CreatePaymentSuccessResponse>("/payments/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...adminHeaders(),
    },
    body: JSON.stringify(payload),
  });
}

export async function postCreateDrop(
  payload: CreateDropRequest,
): Promise<CreateDropSuccessResponse> {
  return request<CreateDropSuccessResponse>("/drops", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...adminHeaders(),
    },
    body: JSON.stringify(payload),
  });
}

/**
 * Contract type only.
 * This helper is intentionally not implemented for browser use because
 * /payments/callback is provider-driven and requires NOWPayments signature headers.
 */
export type PaymentsCallbackHandledResponse = PaymentsCallbackResponse;
