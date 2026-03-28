import { Outlet } from "react-router-dom";
import { ApiStatusBar } from "../components/ApiStatusBar";
import { AppHeader } from "../components/AppHeader";
import type { ThemeMode } from "../hooks/useTheme";

type Props = {
  mode: ThemeMode;
  onThemeToggle: () => void;
};

export function AppLayout({ mode, onThemeToggle }: Props) {
  return (
    <div className="shell">
      <AppHeader mode={mode} onThemeToggle={onThemeToggle} />
      <div className="shell__status">
        <ApiStatusBar />
      </div>
      <main className="shell__main">
        <Outlet />
      </main>
      <footer className="shell__footer">
        <p>
          For research only. Not financial advice. Gambling may be restricted in your region — comply with
          applicable laws and sportsbook terms.
        </p>
      </footer>
    </div>
  );
}
