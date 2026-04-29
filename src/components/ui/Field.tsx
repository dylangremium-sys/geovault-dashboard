import Panel from "@/src/components/ui/Panel";

type FieldProps = {
  label: string;
  value: string | number;
};

export default function Field({ label, value }: FieldProps) {
  return (
    <Panel label={label}>
      <div className="text-2xl text-white">{value}</div>
    </Panel>
  );
}