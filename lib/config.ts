const requiredEnvVars = [
  "GFP_API_BASE_URL",
  "GFP_ADMIN_API_KEY",
  "GFP_TENANT_ID",
] as const;

type RequiredEnvVar = (typeof requiredEnvVars)[number];

type RuntimeConfig = Record<RequiredEnvVar, string>;

function readEnvVar(name: RequiredEnvVar): string {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export function getRuntimeConfig(): RuntimeConfig {
  return {
    GFP_API_BASE_URL: readEnvVar("GFP_API_BASE_URL"),
    GFP_ADMIN_API_KEY: readEnvVar("GFP_ADMIN_API_KEY"),
    GFP_TENANT_ID: readEnvVar("GFP_TENANT_ID"),
  };
}
