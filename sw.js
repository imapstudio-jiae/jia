/* 여백 · 홈 화면 설치용 서비스 워커 (버전 pin2024b · 2026-11-21)
   목적은 두 가지입니다.
   1) 안드로이드가 이 사이트를 '앱처럼 설치'할 수 있게 하는 것
   2) 옛 화면이 남지 않게 하는 것 — 캐시를 쓰지 않고, 브라우저 HTTP 캐시까지
      건너뛰어 항상 네트워크에서 새 파일을 받습니다. */
const VERSION = 'pin2024b-20261121';

self.addEventListener('install', function () {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil((async function () {
    /* 예전 버전이 남긴 캐시를 모두 지운다 */
    try {
      const keys = await caches.keys();
      await Promise.all(keys.map(function (k) { return caches.delete(k); }));
    } catch (e) {}
    await self.clients.claim();
  })());
});

/* 네트워크 우선 + HTTP 캐시 우회.
   같은 사이트 파일은 매번 새로 받고, 오프라인처럼 실패할 때만 브라우저 기본 동작에 맡깁니다.
   다른 사이트(폰트 CDN 등)는 가로채지 않습니다. */
self.addEventListener('fetch', function (event) {
  const req = event.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch (e) { return; }
  if (url.origin !== self.location.origin) return;
  if (url.pathname.endsWith('/sw.js')) return; /* 워커 스크립트는 브라우저가 직접 관리 */

  event.respondWith((async function () {
    try {
      return await fetch(req, { cache: 'reload' });
    } catch (e) {
      try {
        return await fetch(req);
      } catch (e2) {
        return new Response('', { status: 504, statusText: 'offline' });
      }
    }
  })());
});
