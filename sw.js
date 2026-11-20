/* 여백 · 홈 화면 설치용 최소 서비스 워커
   캐시를 전혀 쓰지 않습니다. 모든 요청은 브라우저 기본 동작(네트워크)으로 그대로 갑니다.
   목적은 하나: 안드로이드가 이 사이트를 '앱처럼 설치'할 수 있게 하는 것. */
self.addEventListener('install', function () {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function () {
  /* 가로채지 않음 — 캐시 없음, 항상 최신 화면 */
});
