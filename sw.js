// Service worker for the Sogang Korean flashcards app.
//
// Two different caching jobs, deliberately handled differently:
//
//   shell (index.html)  network-first, so a student picks up a new build on
//                       their next online visit instead of being stuck on a
//                       cached app for weeks. Falls back to cache offline.
//   audio/*.m4a         cache-first and permanent. A clip is immutable — its
//                       filename is a hash of the card it belongs to — so once
//                       fetched there is never a reason to ask the network again.
//                       This is what makes the app work offline for whatever
//                       someone has already studied.
//
// 9cc5c0f82588 is substituted by build.py with a hash of index.html, so a new
// build gets a new shell cache and the old one is deleted on activate.

const VERSION = "9cc5c0f82588";
const SHELL_CACHE = `sogang-shell-${VERSION}`;
const AUDIO_CACHE = "sogang-audio-v1"; // survives shell updates; clips never change

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((c) => c.addAll(["./", "./index.html"]))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        // Drop superseded shells. The audio cache is intentionally spared —
        // re-downloading megabytes of unchanged clips on every deploy would
        // defeat the whole point of splitting them out.
        names.filter((n) => n.startsWith("sogang-shell-") && n !== SHELL_CACHE)
             .map((n) => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.includes("/audio/")) {
    event.respondWith(
      caches.open(AUDIO_CACHE).then((cache) =>
        cache.match(req).then((hit) => {
          if (hit) return hit;
          return fetch(req).then((res) => {
            // Only cache a real hit; caching a 404 would make a missing clip
            // permanently missing even after it is published.
            if (res.ok) cache.put(req, res.clone());
            return res;
          });
        })
      )
    );
    return;
  }

  const isShell = req.mode === "navigate" || url.pathname.endsWith("/index.html");
  if (isShell) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(SHELL_CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((hit) => hit || caches.match("./index.html")))
    );
  }
});
