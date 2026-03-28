import { useMemo, useState } from "react";

const SUGGESTIONS = ["J. Tatum", "L. James", "S. Curry", "G. Antetokounmpo"];

export function FavoritesPage() {
  const [favorites, setFavorites] = useState<string[]>(["J. Tatum"]);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return SUGGESTIONS.filter((s) => !favorites.includes(s));
    return SUGGESTIONS.filter((s) => s.toLowerCase().includes(q) && !favorites.includes(s));
  }, [query, favorites]);

  function add(name: string) {
    setFavorites((f) => (f.includes(name) ? f : [...f, name]));
    setQuery("");
  }

  function remove(name: string) {
    setFavorites((f) => f.filter((x) => x !== name));
  }

  return (
    <div className="page page--narrow">
      <header className="page-hero">
        <p className="page-hero__eyebrow">Watchlist</p>
        <h1 className="page-hero__title">Favorite players</h1>
        <p className="page-hero__lead">
        Track players for quick access and (later) favorites-first sorting on the line board. This list is
        stored in the browser for now; accounts will sync across devices.
        </p>
      </header>

      <div className="field">
        <label htmlFor="fav-search">Add player</label>
        <input
          id="fav-search"
          type="search"
          placeholder="Search name…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoComplete="off"
        />
      </div>

      {filtered.length > 0 ? (
        <ul className="suggest-list">
          {filtered.map((name) => (
            <li key={name}>
              <button type="button" className="btn btn--ghost" onClick={() => add(name)}>
                Add {name}
              </button>
            </li>
          ))}
        </ul>
      ) : null}

      <h2 className="page__h2">Your list</h2>
      {favorites.length === 0 ? (
        <p className="muted">No favorites yet.</p>
      ) : (
        <ul className="fav-list">
          {favorites.map((name) => (
            <li key={name} className="fav-list__row">
              <span>{name}</span>
              <button type="button" className="btn btn--small" onClick={() => remove(name)}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
