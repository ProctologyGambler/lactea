{% load static %}
// Mooo service worker (Tier 1: cache the app shell so the app loads offline).
//
// Strategy:
//   - On install: pre-cache the app shell (HTML pages + static assets).
//   - On fetch:
//       * HTML requests use network-first (fresh when online, cached when offline).
//       * Static asset requests use cache-first (fast, only hits network if missing).
//   - POST/PUT/DELETE are never intercepted — they go straight to the server.
//     (Offline writes are a future "Tier 2" upgrade.)
//
// Cache versioning:
//   When you change anything in the cached list below, bump CACHE_NAME so the
//   old cache is cleared on activate. Otherwise users see stale assets.

const CACHE_NAME = 'mooo-v2';

const APP_SHELL = [
    '{% url "home" %}',
    '{% url "pump_timer" %}',
    '{% url "daily_log" %}',
    '{% url "supplements" %}',
    '{% url "supplement_guide" %}',
    '{% url "progress" %}',
    '{% url "privacy" %}',
    '{% static "js/tailwind.js" %}',
    '{% static "js/chart.min.js" %}',
    '{% static "js/timer.js" %}',
    '{% static "js/charts.js" %}',
    '{% static "images/cow-icon.svg" %}',
    '{% static "images/cow-start.svg" %}',
    '{% static "images/cow-stop.svg" %}',
    '{% static "sounds/mooo.mp3" %}',
    '{% static "manifest.json" %}',
];

// install: download and store the app shell.
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
    );
    // Activate this SW immediately on first install instead of waiting for the
    // previous SW (if any) to stop being used.
    self.skipWaiting();
});

// activate: delete old caches from previous versions.
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((names) =>
            Promise.all(
                names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n))
            )
        ).then(() => self.clients.claim())
    );
});

// fetch: intercept requests and serve from cache or network.
self.addEventListener('fetch', (event) => {
    const req = event.request;

    // Only handle GETs. POSTs (Save Session, etc.) always go to the server.
    if (req.method !== 'GET') return;

    const acceptHeader = req.headers.get('Accept') || '';
    const isHtmlRequest =
        req.mode === 'navigate' || acceptHeader.includes('text/html');

    if (isHtmlRequest) {
        // Network-first for HTML: try to fetch the latest version; fall back to
        // cache if offline. Refresh the cache with whatever we got from the network.
        event.respondWith(
            fetch(req)
                .then((response) => {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
                    return response;
                })
                .catch(() => caches.match(req).then((cached) => cached || caches.match('{% url "home" %}')))
        );
        return;
    }

    // Cache-first for static assets: serve immediately from cache, fall back to
    // network only if the file isn't cached yet.
    event.respondWith(
        caches.match(req).then((cached) => cached || fetch(req))
    );
});
