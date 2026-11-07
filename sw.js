const CACHE = 'biverway-v3';
const ASSETS = [
  '/biverway-lot-size-calculator/',
  '/biverway-lot-size-calculator/index.html',
  '/biverway-lot-size-calculator/icon-512.png',
  '/biverway-lot-size-calculator/manifest.json'
];

// Install: save the app files
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// Activate: delete old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: network first, saved copy only when offline
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request, { cache: 'no-cache' }).then(response => {
      if (response && response.status === 200) {
        const clone = response.clone();
        caches.open(CACHE).then(cache => cache.put(e.request, clone));
      }
      return response;
    }).catch(() =>
      caches.match(e.request).then(cached =>
        cached || caches.match('/biverway-lot-size-calculator/index.html')
      )
    )
  );
});
