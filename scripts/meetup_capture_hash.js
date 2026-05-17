// run: node meetup_capture_hash.js

const { chromium } = require("playwright");

const TARGET_URL =
  process.argv[2] ||
  "https://www.meetup.com/find/?location=us--ny--New+York&source=EVENTS";
const TARGET_OPERATION = process.argv[3] || "recommendedEventsWithSeries";
const TIMEOUT_MS = Number(process.argv[4] || 20000);

function parseMaybeJson(value) {
  if (!value || typeof value !== "string") {
    return null;
  }

  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function getOperationPayload(request) {
  const url = new URL(request.url());
  const method = request.method();

  if (method === "GET") {
    const operationName = url.searchParams.get("operationName");
    const extensions = parseMaybeJson(url.searchParams.get("extensions"));
    return {
      method,
      url: request.url(),
      operationName,
      hash: extensions?.persistedQuery?.sha256Hash || null,
      rawExtensions: extensions,
    };
  }

  const postBody = request.postDataJSON?.() || parseMaybeJson(request.postData());
  return {
    method,
    url: request.url(),
    operationName: postBody?.operationName || null,
    hash: postBody?.extensions?.persistedQuery?.sha256Hash || null,
    rawExtensions: postBody?.extensions || null,
  };
}

function isTargetOperation(operationName) {
  return (
    typeof operationName === "string" &&
    (operationName === TARGET_OPERATION ||
      operationName.startsWith(TARGET_OPERATION) ||
      TARGET_OPERATION.startsWith(operationName))
  );
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1100 },
    serviceWorkers: "block",
  });
  const page = await context.newPage();

  let found = false;

  page.on("request", (request) => {
    const url = request.url();
    if (!url.includes("graphql") && !url.includes("/gql") && !url.includes("operationName=")) {
      return;
    }

    const payload = getOperationPayload(request);
    if (!isTargetOperation(payload.operationName)) {
      return;
    }

    found = true;
    console.log(JSON.stringify(payload, null, 2));
  });

  await page.goto(TARGET_URL, { waitUntil: "domcontentloaded", timeout: TIMEOUT_MS });
  await page.waitForLoadState("networkidle", { timeout: TIMEOUT_MS }).catch(() => {});

  // Trigger lazy requests that may not fire on initial paint.
  await page.mouse.wheel(0, 1800).catch(() => {});
  await page.waitForTimeout(5000);

  await browser.close();

  if (!found) {
    console.error(
      `No matching GraphQL request captured for operation "${TARGET_OPERATION}" within ${TIMEOUT_MS}ms.`
    );
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
