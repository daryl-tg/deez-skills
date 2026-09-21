#!/usr/bin/env bun
// origin-challenge-stub.ts — the loopback origin for features/origin-challenge-backoff.md
//
//   mkdir -p /tmp/origin-stub && cd /tmp/origin-stub
//   echo ok > mode
//   bun ~/.claude/skills/verify-om/helpers/origin-challenge-stub.ts &
//   # flip the window on:   echo challenge > mode
//   # flip it back off:     echo ok > mode
//   # the proof of silence: cat requests.log
//
// It serves an RSS feed whose newest item advances once a minute, article pages
// behind it, and — while the `mode` file reads `challenge` — a Cloudflare-style
// challenge. Every request is appended to requests.log with a UTC timestamp;
// that log, not the lane log, is what proves the daemon went quiet, because a
// held window logs nothing by design.
//
// The challenge shape is load-bearing: the daemon's predicate is a 403 OR 503
// carrying `cf-mitigated: challenge` (packages/cli/src/shared/public-document.ts).
// A stub that returns a bare 403 is never detected and the whole run proves
// nothing, so do not "simplify" the header away.
//
// Port 18111 is this recipe's assigned slot in the agent range 18097-18197.
// Override with ORIGIN_STUB_PORT, staying inside that range.
const PORT = Number(process.env.ORIGIN_STUB_PORT ?? 18111);
const MODE_FILE = "mode";
const LOG_FILE = "requests.log";

const started = Date.now();
const lines: string[] = [];

async function mode(): Promise<string> {
  try {
    return (await Bun.file(MODE_FILE).text()).trim();
  } catch {
    return "ok"; // no mode file yet: serve normally
  }
}

function record(line: string): void {
  lines.push(`${new Date().toISOString()} ${line}`);
  Bun.write(LOG_FILE, `${lines.join("\n")}\n`);
}

function rss(): string {
  const minutes = Math.floor((Date.now() - started) / 60_000) + 1;
  const items = Array.from({ length: Math.min(minutes, 10) }, (_, i) => {
    const n = minutes - i;
    const when = new Date(started + n * 60_000).toUTCString();
    return `<item><title>Stub item ${n}</title><link>http://127.0.0.1:${PORT}/article/${n}</link><guid>stub-${n}</guid><pubDate>${when}</pubDate><description>Item ${n} body</description></item>`;
  }).join("");
  return `<?xml version="1.0"?><rss version="2.0"><channel><title>Origin stub</title><link>http://127.0.0.1:${PORT}/rss</link><description>verify-om origin challenge stub</description>${items}</channel></rss>`;
}

Bun.serve({
  port: PORT,
  hostname: "127.0.0.1", // loopback only; the lane needs OM_FEED_ALLOW_LOOPBACK=1 to reach it
  async fetch(req) {
    const path = new URL(req.url).pathname;
    if ((await mode()) === "challenge") {
      record(`challenge ${req.method} ${path}`);
      return new Response(
        "<html><head><title>Just a moment...</title></head><body>Just a moment...</body></html>",
        { status: 403, headers: { "cf-mitigated": "challenge", "content-type": "text/html" } },
      );
    }
    record(`ok ${req.method} ${path}`);
    if (path === "/rss") {
      return new Response(rss(), { headers: { "content-type": "application/rss+xml" } });
    }
    if (path.startsWith("/article/")) {
      const id = path.split("/").pop();
      return new Response(
        `<html><head><title>Stub item ${id}</title></head><body><article><h1>Stub item ${id}</h1><p>Body of item ${id}.</p></article></body></html>`,
        { headers: { "content-type": "text/html" } },
      );
    }
    return new Response("stub ok", { headers: { "content-type": "text/plain" } });
  },
});
console.log(`origin stub listening on http://127.0.0.1:${PORT}`);
