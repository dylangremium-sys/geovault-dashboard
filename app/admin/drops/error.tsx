"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <main style={{ padding: "24px", fontFamily: "sans-serif" }}>
      <h1>Failed to load drops</h1>
      <p>{error.message}</p>
      <button type="button" onClick={() => reset()}>
        Retry
      </button>
    </main>
  );
}
