import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const appRoot = fileURLToPath(new URL("..", import.meta.url));
const port = process.env.MTBUDDY_UI_SMOKE_PORT ?? "5174";
const url = `http://127.0.0.1:${port}/`;
const expectedTitle = "MTBUDDY，我帮你";
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
    const sidebar = document.querySelector(".sidebar");

    return {
      title: document.querySelector("h1")?.textContent ?? "",
      bodyWidth: document.body.scrollWidth,
      viewportWidth: window.innerWidth,
      navItems: document.querySelectorAll(".nav-item").length,
      quickChips: document.querySelectorAll(".quick-chip").length,
      composerVisible: Boolean(document.querySelector(".composer-card")),
      workspaceVisible: Boolean(document.querySelector(".workspace-picker")),
      sidebarVisible: sidebar ? getComputedStyle(sidebar).display !== "none" : false,
      horizontalOverflow: document.body.scrollWidth > window.innerWidth + 1
    };
  });

  await page.close();

  if (metrics.title !== expectedTitle) {
    fail(`Unexpected title for ${target.name}: ${metrics.title}`);
  }

  if (target.width >= 820 && metrics.navItems !== 6) {
    fail(`Expected 6 sidebar nav items for ${target.name}, saw ${metrics.navItems}.`);
  }

  if (metrics.quickChips < 8) {
    fail(`Expected at least 8 quick chips for ${target.name}, saw ${metrics.quickChips}.`);
  }

  if (!metrics.composerVisible || !metrics.workspaceVisible) {
    fail(`Composer or workspace picker missing for ${target.name}.`);
  }

  if (metrics.horizontalOverflow) {
    fail(`Detected horizontal overflow for ${target.name}.`);
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
