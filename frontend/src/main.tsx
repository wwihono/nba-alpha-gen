import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { applyThemeToDocument, getInitialTheme } from "./hooks/useTheme";
import "./index.css";
import App from "./App.tsx";

applyThemeToDocument(getInitialTheme());

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
