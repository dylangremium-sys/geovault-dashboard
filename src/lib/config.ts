export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.trim() || "http://127.0.0.1:8000";

export const ADMIN_API_KEY =
  process.env.NEXT_PUBLIC_ADMIN_API_KEY?.trim() || "";

export const TENANT_ID =
  process.env.NEXT_PUBLIC_TENANT_ID?.trim() || "";
