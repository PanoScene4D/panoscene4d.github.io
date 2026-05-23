import { version as appVersion } from '../package.json';

// export default null
declare let self: ServiceWorkerGlobalScope;

self.addEventListener('install', (event) => {
    console.log(`installing v${appVersion}`);
    self.skipWaiting();
    event.waitUntil(
        caches.keys().then((names) => Promise.all(names.map((name) => caches.delete(name))))
    );
});

self.addEventListener('activate', (event) => {
    console.log(`activating v${appVersion}`);
    event.waitUntil(
        caches.keys()
        .then((names) => Promise.all(names.map((name) => caches.delete(name))))
        .then(() => self.clients.claim())
    );
});
