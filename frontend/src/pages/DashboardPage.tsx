import { SectionCard } from "../components/SectionCard";

const mockGames = [
  { id: "1", matchup: "LAL @ BOS", time: "7:30 PM ET", streaks: "LAL W2 · BOS L1" },
  { id: "2", matchup: "MIA vs NYK", time: "8:00 PM ET", streaks: "MIA W1 · NYK W3" },
];

const mockProps = [
  { player: "J. Tatum", market: "PTS O/U", line: "27.5", risk: "Medium", edge: "—" },
  { player: "L. James", market: "PTS O/U", line: "24.5", risk: "Low", edge: "—" },
];

export function DashboardPage() {
  return (
    <div className="dashboard">
      <section className="hero" aria-labelledby="hero-title">
        <p className="hero__eyebrow">Live odds · Props · Risk</p>
        <h1 id="hero-title" className="hero__title">
          NBA edge dashboard
        </h1>
        <p className="hero__lead">
          Research-grade view of schedules, lines, and context—built with the same clarity as modern fintech
          surfaces. Connect data feeds and models to activate picks, simulations, and exports.
        </p>
      </section>

      <nav className="dashboard__jump" aria-label="Section shortcuts">
        <span className="dashboard__jump-label">Jump to</span>
        <a href="#slate">Slate</a>
        <a href="#game-detail">Game analysis</a>
        <a href="#injury">Injuries</a>
        <a href="#props">Prop lines</a>
        <a href="#picks">Picks</a>
        <a href="#data-health">Data health</a>
      </nav>

      <SectionCard
        id="slate"
        title="Today / slate"
        subtitle="Games, start times, rest and travel (coming with schedule ingest)."
        badge="Slate"
      >
        <ul className="slate-list">
          {mockGames.map((g) => (
            <li key={g.id} className="slate-list__row">
              <div>
                <strong>{g.matchup}</strong>
                <span className="muted">{g.time}</span>
              </div>
              <span className="slate-list__streak">{g.streaks}</span>
            </li>
          ))}
        </ul>
      </SectionCard>

      <SectionCard
        id="game-detail"
        title="Game props & matchup"
        subtitle="Home court, H2H, defensive matchup, momentum, 100-game sim vs market spread."
        badge="Game"
      >
        <div className="game-preview">
          <p>
            <strong>Selected:</strong> LAL @ BOS — placeholder until game APIs are connected.
          </p>
          <ul className="game-preview__list">
            <li>Home court boost & home/away records</li>
            <li>H2H: last meetings, margin, pace (small-sample warnings)</li>
            <li>Defensive schemes / pace clash</li>
            <li>Momentum: win/loss streak entering tip</li>
            <li>
              <button type="button" className="btn btn--secondary" disabled>
                Run 100-game simulation
              </button>{" "}
              <span className="muted">(Monte Carlo — model TBD)</span>
            </li>
          </ul>
        </div>
      </SectionCard>

      <SectionCard
        id="injury"
        title="Injury pulse"
        subtitle="Recent status changes and projected minutes impact."
        badge="Injuries"
      >
        <p className="muted">No injury feed connected yet. This panel will list deltas in the last N hours.</p>
      </SectionCard>

      <SectionCard
        id="props"
        title="Player prop line board"
        subtitle="Multi-book snapshots, best price, movement, risk tier, steam flags."
        badge="Props"
      >
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Player</th>
                <th>Market</th>
                <th>Line</th>
                <th>Risk</th>
                <th>Edge</th>
              </tr>
            </thead>
            <tbody>
              {mockProps.map((row) => (
                <tr key={row.player + row.market}>
                  <td>{row.player}</td>
                  <td>{row.market}</td>
                  <td>{row.line}</td>
                  <td>
                    <span className={`risk-pill risk-pill--${row.risk === "Low" ? "low" : "mid"}`}>
                      {row.risk}
                    </span>
                  </td>
                  <td>{row.edge}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="muted small">
          Filters: risk band, pick vs lock tier, show auto-blacklisted (hidden by default after 3+ consecutive
          prop misses).
        </p>
      </SectionCard>

      <SectionCard
        id="picks"
        title="Daily picks / locks"
        subtitle="Ranked edges with auditable model and odds snapshot ids."
        badge="Picks"
      >
        <p className="muted">Pick list appears when the ML + odds pipeline is connected.</p>
      </SectionCard>

      <SectionCard
        id="reports"
        title="Reasoning & reports"
        subtitle="Line-level reasoning and exportable slate / per-game reports."
        badge="Reports"
      >
        <p className="muted">Structured reasoning drawer and PDF/HTML export — upcoming.</p>
      </SectionCard>

      <SectionCard
        id="data-health"
        title="Data health"
        subtitle="Last successful sync per source and per book."
        badge="Ops"
      >
        <ul className="health-list">
          <li>
            <span>API</span>
            <span className="health-list__ok">Reachable (see status bar)</span>
          </li>
          <li>
            <span>Odds poller</span>
            <span className="muted">Not configured</span>
          </li>
          <li>
            <span>Injuries</span>
            <span className="muted">Not configured</span>
          </li>
        </ul>
      </SectionCard>
    </div>
  );
}
