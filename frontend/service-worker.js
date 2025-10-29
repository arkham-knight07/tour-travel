const CACHE = "travelmate-v2";
const ASSETS = [
  "/", "/index.html",
  "/styles/main.css",
  "/scripts/api.js", "/scripts/main.js", "/scripts/chatbot.js",
  "/data/tours.json", "/data/faq.json",
  "/pages/about_us.html", "/pages/booking.html",
  "/fonts/Montserrat-Bold.woff2",
  // Add more assets as needed
];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(r => {
      if (r) return r;
      return fetch(e.request).then(resp => {
        // Only cache basic, same-origin requests
        if (resp.ok && resp.type === "basic") {
          const copy = resp.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return resp;
      }).catch(() => caches.match("/index.html"));
    })
  );
});