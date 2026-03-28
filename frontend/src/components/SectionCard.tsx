import type { ReactNode } from "react";

type Props = {
  id?: string;
  title: string;
  subtitle?: string;
  badge?: string;
  children: ReactNode;
};

export function SectionCard({ id, title, subtitle, badge, children }: Props) {
  return (
    <section className="section-card" id={id}>
      <header className="section-card__head">
        <div>
          <h2 className="section-card__title">{title}</h2>
          {subtitle ? <p className="section-card__sub">{subtitle}</p> : null}
        </div>
        {badge ? <span className="section-card__badge">{badge}</span> : null}
      </header>
      <div className="section-card__body">{children}</div>
    </section>
  );
}
