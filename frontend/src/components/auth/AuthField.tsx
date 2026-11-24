export function AuthField({
  label,
  name,
  type = "text",
  value,
  onChange,
  autoComplete,
}: {
  label: string;
  name: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  autoComplete?: string;
}) {
  return (
    <label className="block text-sm font-medium text-primary" htmlFor={name}>
      {label}
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        autoComplete={autoComplete}
        className="mt-2 block w-full rounded-lg border border-border bg-white px-3 py-2.5 text-primary outline-none focus:border-primary-blue focus:ring-2 focus:ring-light-blue"
      />
    </label>
  );
}
