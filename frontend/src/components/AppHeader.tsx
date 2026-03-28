import { NavLink } from "react-router-dom";
import type { ThemeMode } from "../hooks/useTheme";
import { ThemeToggle } from "./ThemeToggle";

type Props = {
  mode: ThemeMode;
  onThemeToggle: () => void;
};

const navClass = ({ isActive }: { isActive: boolean }) =>
  "app-header__link" + (isActive ? " app-header__link--active" : "");

export function AppHeader({ mode, onThemeToggle }: Props) {
  return (
    <header className="app-header">
      <div className="app-header__brand">
        <span className="app-header__logo" aria-hidden>
          ◆
        </span>
        <div>
          <span className="app-header__name">NBA Alpha Gen</span>
          <span className="app-header__tag">Edge dashboard</span>
        </div>
      </div>
      <nav className="app-header__nav" aria-label="Main">
        <NavLink to="/" end className={navClass}>
          Dashboard
        </NavLink>
        <NavLink to="/favorites" className={navClass}>
          Favorites
        </NavLink>
        <NavLink to="/settings" className={navClass}>
          Settings
        </NavLink>
      </nav>
      <ThemeToggle mode={mode} onToggle={onThemeToggle} />
    </header>
  );
}
