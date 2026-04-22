export type HealthResponse = {
  status: "ok";
};

export type RootResponse = {
  message: "GeoVault Protocol API running";
};

export type NearbyDropListItem = {
  id: number;
  distance_km: number;
  status: "active";
};

export type AdminDropItem = {
  id: number;
  w3w_address: string;
  lat: number;
  lng: number;
  price_crypto: number;
  is_claimed: boolean;
  product_id: string | null;
};

export type AdminDropsResponse = {
  status: "success";
  count: number;
  items: AdminDropItem[];
};

export type AdminEntitlementItem = {
  id: number;
  drop_id: number;
  payment_id: string;
  is_used: boolean;
  expires_at: string | null;
  created_at: string | null;
};

export type AdminEntitlementsResponse = {
  status: "success";
  count: number;
  items: AdminEntitlementItem[];
};

export type AdminSummary = {
  total_drops: number;
  claimed_drops: number;
  total_entitlements: number;
  used_entitlements: number;
};

export type AdminSummaryResponse = {
  status: "success";
  summary: AdminSummary;
};

export type ClaimRequest = {
  drop_id: number;
  lat: number;
  lng: number;
  entitlement_token: string;
};

export type ClaimSuccessResponse = {
  status: "success";
  distance_m: number;
  drop_id: number;
};

export type ClaimOutOfRangeResponse = {
  status: "out_of_range";
  distance_m: number;
};

export type ClaimResponse =
  | ClaimSuccessResponse
  | ClaimOutOfRangeResponse;

export type RevealRequest = {
  drop_id: number;
  entitlement_token: string;
};

export type RevealSuccessResponse = {
  status: "success";
  drop_id: number;
  w3w_address: string;
  product_id: string | null;
};

export type CreatePaymentRequest = {
  drop_id: number;
  price_currency: "usd";
  pay_currency: "btc";
};

export type CreatePaymentSuccessResponse = {
  status: "success";
  drop_id: number;
  price_used: number;
  invoice: Record<string, unknown>;
};

export type PaymentsCallbackIgnoredResponse = {
  status: "ignored";
  payment_status: string | null;
};

export type PaymentsCallbackAlreadyProcessedResponse = {
  status: "already_processed";
  drop_id: number;
  payment_id: string;
  entitlement_id: number;
};

export type PaymentsCallbackEntitlementIssuedResponse = {
  status: "entitlement_issued";
  drop_id: number;
  payment_id: string;
  entitlement_id: number;
};

export type PaymentsCallbackResponse =
  | PaymentsCallbackIgnoredResponse
  | PaymentsCallbackAlreadyProcessedResponse
  | PaymentsCallbackEntitlementIssuedResponse;
