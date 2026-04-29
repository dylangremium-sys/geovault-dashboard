type SectionTitleProps = {
    children: string;
  };
  
  export default function SectionTitle({ children }: SectionTitleProps) {
    return (
      <div className="mb-4 text-xs uppercase tracking-[0.2em] text-neutral-500">
        {children}
      </div>
    );
  }