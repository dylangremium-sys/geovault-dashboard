type DataTableProps = {
    headers: string[];
    rows: React.ReactNode;
  };
  
  export default function DataTable({ headers, rows }: DataTableProps) {
    return (
      <div className="overflow-x-auto border border-neutral-800 bg-neutral-950">
        <table className="min-w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-neutral-800 text-left text-neutral-500">
              {headers.map((header) => (
                <th key={header} className="px-4 py-3 font-medium">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    );
  }