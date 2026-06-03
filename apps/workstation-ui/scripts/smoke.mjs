import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const appRoot = fileURLToPath(new URL("..", import.meta.url));
const port = process.env.MTBUDDY_UI_SMOKE_PORT ?? "5174";
const url = `http://127.0.0.1:${port}/`;
const expectedTitle = "Summarize these files and create an action list";
const serverLogs = [];

const server = spawn(
  process.execPath,
  ["node_modules/vite/bin/vite.js", "--host", "127.0.0.1", "--port", port, "--strictPort"],
  {
    cwd: appRoot,
    stdio: ["ignore", "pipe", "pipe"]
  }
);

server.stdout.on("data", (chunk) => serverLogs.push(chunk.toString()));
server.stderr.on("data", (chunk) => serverLogs.push(chunk.toString()));

function fail(message) {
  throw new Error(`${message}\n${serverLogs.join("")}`);
}

async function waitForServer() {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    if (server.exitCode !== null) {
      fail(`Vite exited before ${url} became available.`);
    }

    try {
      const response = await fetch(url);
      if (response.ok) {
        return;
      }
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }

  fail(`Timed out waiting for ${url}.`);
}

async function inspectViewport(browser, target) {
  const page = await browser.newPage({ viewport: { width: target.width, height: target.height } });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.screenshot({ path: target.path, fullPage: true });

  const metrics = await page.evaluate(() => {
    const preview = document.querySelector(".preview-panel")?.getBoundingClientRect();
    const rail = document.querySelector(".artifact-rail")?.getBoundingClientRect();

    return {
      title: document.querySelector("h1")?.textContent ?? "",
      bodyWidth: document.body.scrollWidth,
      viewportWidth: window.innerWidth,
      visiblePanels: document.querySelectorAll(".panel").length,
      artifactItems: document.querySelectorAll(".artifact-item").length,
      horizontalOverflow: document.body.scrollWidth > window.innerWidth + 1,
      previewRailGap:
        preview && rail && window.innerWidth >= 1180 ? Math.round(rail.left - preview.right) : null
    };
  });

  await page.close();

  if (metrics.title !== expectedTitle) {
    fail(`Unexpected title for ${target.name}: ${metrics.title}`);
  }

  if (metrics.artifactItems !== 4) {
    fail(`Expected 4 artifact items for ${target.name}, saw ${metrics.artifactItems}.`);
  }

  if (metrics.visiblePanels < 7) {
    fail(`Expected at least 7 panels for ${target.name}, saw ${metrics.visiblePanels}.`);
  }

  if (metrics.horizontalOverflow) {
    fail(`Detected horizontal overflow for ${target.name}.`);
  }

  if (metrics.previewRailGap !== null && metrics.previewRailGap < 10) {
    fail(`Preview and artifact rail are too close for ${target.name}: ${metrics.previewRailGap}px.`);
  }

  if (!existsSync(target.path)) {
    fail(`Screenshot was not written for ${target.name}: ${target.path}`);
  }

  return { ...target, ...metrics };
}

try {
  await waitForServer();

  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const target of [
    {
      name: "desktop",
      width: 1440,
      height: 960,
      path: join(tmpdir(), "mtbuddy-ui-smoke-desktop.png")
    },
    {
      name: "mobile",
      width: 390,
      height: 900,
      path: join(tmpdir(), "mtbuddy-ui-smoke-mobile.png")
    }
  ]) {
    results.push(await inspectViewport(browser, target));
  }

  await browser.close();
  console.log(JSON.stringify({ url, results }, null, 2));
} finally {
  server.kill();
}
