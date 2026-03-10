const CACHE = 'biverway-v2';
const ASSETS = [
  '/biverway-lot-size-calculator/',
  '/biverway-lot-size-calculator/index.html',
  '/biverway-lot-size-calculator/logo.png',
  '/biverway-lot-size-calculator/manifest.json',
  '/biverway-lot-size-calculator/sw.js'
];

// Install — cache everything immediately
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate — clear old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch — cache first, then network
self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        if (!response || response.status !== 200) return response;
        const clone = response.clone();
        caches.open(CACHE).then(cache => cache.put(e.request, clone));
        return response;
      }).catch(() => caches.match('/biverway-lot-size-calculator/index.html'));
    })
  );
});
