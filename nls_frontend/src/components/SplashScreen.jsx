import { useState, useEffect, useCallback } from "react";
import { getSplash } from "../services/getApi";
import "./SplashScreen.css";

const SESSION_KEY = "nls_splash_seen";

const SplashScreen = () => {
  const [splash, setSplash] = useState(null);

  const dismiss = useCallback(() => {
    setSplash(null);
  }, []);

  useEffect(() => {
    if (sessionStorage.getItem(SESSION_KEY)) return;

    let mounted = true;
    const load = async () => {
      try {
        const data = await getSplash();
        if (!mounted) return;
        if (!data || (Array.isArray(data) && data.length === 0)) return;
        if (!data.image) return;
        setSplash(data);
        sessionStorage.setItem(SESSION_KEY, "1");
      } catch {
        return;
      }
    };
    load();
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (!splash) return;
    const onKey = (e) => {
      if (e.key === "Escape") dismiss();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [splash, dismiss]);

  if (!splash) return null;

  const BASE = import.meta.env.VITE_API_BASE ?? "";
  const src = splash.image.startsWith("http")
    ? splash.image
    : `${BASE}${splash.image}`;

  const imageEl = (
    <img
      src={src}
      alt={splash.title || "Announcement"}
      className="splash-modal__image"
      onError={dismiss}
    />
  );

  return (
    <div
      className="splash-backdrop"
      onClick={dismiss}
      role="presentation"
    >
      <div
        className="splash-modal"
        role="dialog"
        aria-modal="true"
        aria-label={splash.title || "Announcement"}
        onClick={(e) => e.stopPropagation()}
      >
        <button
          type="button"
          className="splash-modal__close"
          aria-label="Close announcement"
          onClick={dismiss}
          autoFocus
        >
          {"\u00D7"}
        </button>
        {splash.link_url ? (
          <a
            href={splash.link_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
          >
            {imageEl}
          </a>
        ) : (
          imageEl
        )}
      </div>
    </div>
  );
};

export default SplashScreen;
