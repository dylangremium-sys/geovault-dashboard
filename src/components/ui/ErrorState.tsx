type ErrorStateProps = {
    message: string;
  };
  
  export default function ErrorState({ message }: ErrorStateProps) {
    return (
      <section className="border border-red-900 bg-red-950/30 p-4">
        <div className="text-xs uppercase tracking-wide text-red-400">Error</div>
        <div className="mt-2 text-sm text-red-200">{message}</div>
      </section>
    );
  }