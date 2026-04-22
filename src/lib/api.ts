import { API_BASE_URL, ADMIN_API_KEY } from "./config";
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
    const text = await response.text();
    throw new Error(`API request failed: ${response.status} ${text}`);
  }

  return response.json() as Promise<T>;
}

function adminHeaders(): Record<string, string> {
  return ADMIN_API_KEY ? { "x-api-key": ADMIN_API_KEY } : {};
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
  const search = new URLSearchParams({
    w3w_address: payload.w3w_address,
    lat: String(payload.lat),
    lng: String(payload.lng),
    price_crypto: String(payload.price_crypto),
  });

  return request<CreateDropSuccessResponse>(`/drops?${search.toString()}`, {
    method: "POST",
    headers: {
      ...adminHeaders(),
    },
  });
}

/**
 * Contract type only.
 * This helper is intentionally not implemented for browser use because
 * /payments/callback is provider-driven and requires NOWPayments signature headers.
 */
export type PaymentsCallbackHandledResponse = PaymentsCallbackResponse;
