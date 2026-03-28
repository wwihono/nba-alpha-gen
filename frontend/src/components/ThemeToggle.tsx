import type { ThemeMode } from "../hooks/useTheme";

type Props = {
  mode: ThemeMode;
  onToggle: () => void;
};

export function ThemeToggle({ mode, onToggle }: Props) {
  const label = mode === "dark" ? "Switch to light interface" : "Switch to dark interface";
  return (
    <button type="button" className="theme-toggle" onClick={onToggle} aria-label={label} title={label}>
      <span className="theme-toggle__track" aria-hidden>
        <span className="theme-toggle__thumb" />
      </span>
      <span className="theme-toggle__text">{mode === "dark" ? "Dark" : "Light"}</span>
    </button>
  );
}
