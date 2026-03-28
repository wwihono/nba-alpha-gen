export function SettingsPage() {
  return (
    <div className="page page--narrow">
      <header className="page-hero">
        <p className="page-hero__eyebrow">Preferences</p>
        <h1 className="page-hero__title">Settings</h1>
        <p className="page-hero__lead">
          Theme uses the toggle in the header (light / dark). Both modes keep a navy-forward brand accent.
        </p>
      </header>

      <section className="settings-block">
        <h2 className="page__h2">Auto-blacklist</h2>
        <p>
          Players who miss a tracked prop <strong>3+ consecutive</strong> games will be hidden from main
          recommendations. You’ll be able to restore or snooze from here once grading is live.
        </p>
        <p className="muted small">No graded props yet — nothing blacklisted.</p>
      </section>

      <section className="settings-block">
        <h2 className="page__h2">API</h2>
        <p>
          Backend URL is set with <code className="inline-code">VITE_API_URL</code> in{" "}
          <code className="inline-code">frontend/.env</code>. Restart the dev server after changing it.
        </p>
      </section>
    </div>
  );
}
