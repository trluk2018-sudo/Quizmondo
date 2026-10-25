// Quizmondo Service Worker for PWA Installation & Push Notifications
const CACHE_NAME = 'quizmondo-v1';
const STATIC_ASSETS = [
  '/',
  '/arena',
  '/static/css/tailwind.min.css',
  '/static/img/quizmondo_logo.svg',
  '/static/img/quizmondo_icon.svg',
  '/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => console.log('PWA cache prefetch note:', err));
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Network first with cache fallback for static assets
  if (event.request.method === 'GET' && (event.request.url.includes('/static/') || event.request.url.endsWith('.svg'))) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, response.clone());
            return response;
          });
        });
      })
    );
  }
});

// Push notification listener (e.g. "It's your turn!")
self.addEventListener('push', (event) => {
  let data = { title: 'Quizmondo Arena', body: "It's your turn in the trivia duel!", url: '/arena' };
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data.body = event.data.text();
    }
  }

  const options = {
    body: data.body,
    icon: '/static/img/quizmondo_icon.svg',
    badge: '/static/img/quizmondo_icon.svg',
    vibrate: [100, 50, 100],
    data: { url: data.url || '/arena' }
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const targetUrl = event.notification.data ? event.notification.data.url : '/arena';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes('/arena') && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
