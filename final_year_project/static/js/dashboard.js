async function loadDashboardSummary() {
  const response = await fetch("/api/dashboard/summary", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error("Unable to load dashboard summary");
  }

  return response.json();
}

function ensureOwnerBanner() {
  if (document.querySelector(".owner-banner")) {
    return;
  }

  const mainContent = document.querySelector(".main-content");
  if (!mainContent) {
    return;
  }

  const banner = document.createElement("section");
  banner.className = "owner-banner";
  banner.setAttribute("aria-label", "Project owners");

  const content = document.createElement("div");
  const label = document.createElement("span");
  const title = document.createElement("h2");

  label.textContent = "Project Owner";
  title.textContent = "Saran (43140029) & Harish Ragavan (43140046)";

  content.append(label, title);
  banner.appendChild(content);
  mainContent.prepend(banner);
}

function createElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) {
    element.className = className;
  }
  if (text !== undefined) {
    element.textContent = text;
  }
  return element;
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value;
  }
}

function statusLabel(status) {
  return status.replaceAll("_", " ");
}

function renderAlerts(alerts) {
  const alertBand = document.getElementById("alerts");
  if (!alertBand) {
    return;
  }

  alertBand.innerHTML = "";

  for (const alert of alerts) {
    alertBand.appendChild(createElement("div", "alert-item", alert));
  }
}

function renderMetrics(metrics) {
  const metricGrid = document.getElementById("overview");
  if (!metricGrid) {
    return;
  }

  metricGrid.innerHTML = "";

  for (const metric of metrics) {
    const card = createElement("article", "metric-card");
    card.appendChild(createElement("span", "metric-label", metric.label));

    const valueRow = createElement("div", "metric-value-row");
    valueRow.appendChild(createElement("strong", "metric-value", metric.value));
    valueRow.appendChild(createElement("span", "metric-unit", metric.unit));
    card.appendChild(valueRow);

    card.appendChild(createElement("span", "metric-trend", metric.trend));
    metricGrid.appendChild(card);
  }
}

function renderCameras(cameras) {
  const cameraGrid = document.getElementById("cameraGrid");
  if (!cameraGrid) {
    return;
  }

  cameraGrid.innerHTML = "";

  for (const camera of cameras) {
    const card = createElement("article", "camera-card");
    card.appendChild(createElement("div", "camera-preview"));

    const body = createElement("div", "camera-body");
    const titleRow = createElement("div", "camera-title-row");
    titleRow.appendChild(createElement("strong", "", camera.name));
    titleRow.appendChild(createElement("span", `state state-${camera.status}`, statusLabel(camera.status)));
    body.appendChild(titleRow);
    body.appendChild(createElement("p", "page-subtitle", camera.location));

    const meta = createElement("div", "camera-meta");
    meta.appendChild(createElement("span", "", `${camera.fps} FPS`));
    meta.appendChild(createElement("span", "", `${camera.confidence}%`));
    meta.appendChild(createElement("span", "", camera.last_seen));
    body.appendChild(meta);

    card.appendChild(body);
    cameraGrid.appendChild(card);
  }
}

function renderEvents(events) {
  const eventList = document.getElementById("eventList");
  if (!eventList) {
    return;
  }

  eventList.innerHTML = "";

  if (events.length === 0) {
    const row = createElement("article", "event-row");
    row.appendChild(createElement("span", "event-dot event-dot-warning"));
    const body = createElement("div");
    body.appendChild(createElement("strong", "", "No tracking events yet"));
    body.appendChild(createElement("p", "", "Connect and configure the camera to start recording entries and exits."));
    row.appendChild(body);
    eventList.appendChild(row);
    return;
  }

  for (const event of events) {
    const row = createElement("article", "event-row");
    row.appendChild(createElement("span", `event-dot event-dot-${event.severity}`));

    const body = createElement("div");
    body.appendChild(createElement("strong", "", `${event.event_type.toUpperCase()} - ${event.bus_number}`));
    body.appendChild(
      createElement(
        "p",
        "",
        `${event.gate} at ${event.occurred_at} - ${event.confidence}% confidence`,
      ),
    );
    row.appendChild(body);
    eventList.appendChild(row);
  }
}

function renderFlowChart(hourlyFlow) {
  const chart = document.getElementById("flowChart");
  if (!chart) {
    return;
  }

  chart.innerHTML = "";
  const maxValue = Math.max(...hourlyFlow.flatMap((flow) => [flow.entries, flow.exits]), 1);

  for (const flow of hourlyFlow) {
    const row = createElement("div", "flow-row");
    row.appendChild(createElement("span", "", flow.hour));

    const stack = createElement("div", "bar-stack");
    const entryBar = createElement("div", "bar bar-entry");
    const exitBar = createElement("div", "bar bar-exit");
    entryBar.style.width = `${(flow.entries / maxValue) * 100}%`;
    exitBar.style.width = `${(flow.exits / maxValue) * 100}%`;
    stack.append(entryBar, exitBar);
    row.appendChild(stack);

    row.appendChild(createElement("span", "flow-count", `${flow.entries}/${flow.exits}`));
    chart.appendChild(row);
  }
}

function renderModules(modules) {
  const moduleGrid = document.getElementById("moduleGrid");
  if (!moduleGrid) {
    return;
  }

  moduleGrid.innerHTML = "";

  for (const module of modules) {
    const card = createElement("article", "module-card");
    card.appendChild(createElement("strong", "", module.name));
    card.appendChild(createElement("span", `state state-${module.status}`, statusLabel(module.status)));
    card.appendChild(createElement("p", "", module.detail));

    const track = createElement("div", "progress-track");
    const bar = createElement("div", "progress-bar");
    bar.style.width = `${module.progress}%`;
    track.appendChild(bar);
    card.appendChild(track);

    moduleGrid.appendChild(card);
  }
}

async function initializeDashboard() {
  const refreshButton = document.getElementById("refreshButton");

  try {
    if (refreshButton) {
      refreshButton.disabled = true;
      refreshButton.textContent = "Refreshing";
    }

    const summary = await loadDashboardSummary();

    setText("systemStatus", summary.system_status);
    setText("occupancyValue", summary.occupancy);
    renderAlerts(summary.alerts);
    renderMetrics(summary.metrics);
    renderCameras(summary.cameras);
    renderEvents(summary.events);
    renderFlowChart(summary.hourly_flow);
    renderModules(summary.modules);
  } catch (error) {
    setText("systemStatus", "offline");
    renderAlerts(["Dashboard API is unavailable. Check the Flask server logs."]);
    console.error(error);
  } finally {
    if (refreshButton) {
      refreshButton.disabled = false;
      refreshButton.textContent = "Refresh";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  ensureOwnerBanner();

  const refreshButton = document.getElementById("refreshButton");
  if (refreshButton) {
    refreshButton.addEventListener("click", initializeDashboard);
  }

  initializeDashboard();
  window.setInterval(initializeDashboard, 30000);
});
