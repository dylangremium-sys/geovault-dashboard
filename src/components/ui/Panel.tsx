type PanelProps = {
    label: string;
    children: React.ReactNode;
  };
  
  export default function Panel({ label, children }: PanelProps) {
    return (
      <div className="border border-neutral-800 bg-neutral-950 p-4">
        <div className="text-xs uppercase tracking-wide text-neutral-500">
          {label}
        </div>
        <div className="mt-2">{children}</div>
      </div>
    );
  }