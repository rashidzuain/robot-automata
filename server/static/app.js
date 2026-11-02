"use strict";

(() => {
  const $ = (id) => document.getElementById(id);
  const state = { source: "device", initialized: false, status: null, polling: false, pending: false, writing: false, timer: null, online: false };
  const number = (value, digits = 1) => typeof value === "number" && Number.isFinite(value) ? value.toLocaleString("es-AR", { minimumFractionDigits: digits, maximumFractionDigits: digits }) : "—";
  const logical = (value) => value === true ? "ALTO (1)" : value === false ? "BAJO (0)" : "—";
  const date = (value, compact = false) => {
    if (!value) return "—";
    const parsed = new Date(value);
    return Number.isNaN(parsed.getTime()) ? "—" : parsed.toLocaleString("es-AR", compact ? { hour: "2-digit", minute: "2-digit", second: "2-digit" } : { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" });
  };

  async function request(path, options = {}) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 7000);
    try {
      const response = await fetch(path, { ...options, cache: "no-store", signal: controller.signal });
      if (!response.ok) throw new Error(`El servidor respondió con error ${response.status}.`);
      return await response.json();
    } finally { clearTimeout(timeout); }
  }

  function renderSource() {
    const demo = state.source === "demo";
    $("source-device").setAttribute("aria-pressed", String(!demo));
    $("source-demo").setAttribute("aria-pressed", String(demo));
    $("source-caption").textContent = demo ? "Datos de ejemplo, separados del robot real" : "Lecturas enviadas por tu robot";
    $("chart-source").textContent = demo ? "SIMULACIÓN" : "ROBOT REAL";
    $("history-description").textContent = demo ? "Datos de ejemplo guardados por el servidor" : "Datos recibidos del robot real";
    $("demo-notice").hidden = !demo;
    $("demo-notice-text").textContent = state.status?.demo_running
      ? "Datos de ejemplo generados por el servidor. No representan mediciones del robot ni mueven los motores."
      : "Simulación detenida. Podés revisar el historial; estas lecturas son de ejemplo y no provienen del robot.";
    $("chart-empty-text").textContent = demo ? "Iniciá una simulación para ver datos de ejemplo en este panel." : "Conectá el robot o iniciá una simulación para explorar el panel.";
  }

  function renderStatus() {
    const status = state.status;
    if (!status) return;
    $("version").textContent = `v${status.version}`;
    $("device-status").textContent = status.device.connected ? "Conectado" : "Sin conexión";
    $("device-status").className = `small-badge ${status.device.connected ? "connected" : "neutral"}`;
    $("device-description").textContent = status.device.connected
      ? `Recibiendo información de ${status.device.robot_id}.`
      : status.device.last_seen_at ? `${status.device.robot_id} no está enviando datos actualmente.` : `Esperando la primera conexión de ${status.device.robot_id}.`;
    $("last-seen").textContent = status.device.last_seen_at ? date(status.device.last_seen_at) : "Todavía no hay datos";
    $("sample-count").textContent = `${Number(status.sample_count).toLocaleString("es-AR")} muestras guardadas en total`;
    $("demo-button-text").textContent = status.demo_running ? "Detener simulación" : "Iniciar simulación";
    $("demo-button").setAttribute("aria-label", status.demo_running ? "Detener simulación" : "Iniciar simulación");
    renderSource();
  }

  function connection(ok) {
    state.online = ok;
    document.body.dataset.offline = String(!ok);
    $("connection-error").hidden = ok;
    $("server-status").className = `status-pill ${ok ? "" : "offline"}`;
    $("server-status-text").textContent = ok ? "Servidor en línea" : "Servidor sin respuesta";
    $("demo-button").disabled = !ok || state.writing;
    if (!ok) {
      $("device-status").textContent = "Sin verificar";
      $("device-status").className = "small-badge neutral";
      $("device-description").textContent = "No se puede verificar el estado del robot hasta recuperar el servidor.";
    }
  }

  function renderTelemetry(data) {
    const items = Array.isArray(data.items) ? data.items : [];
    const current = items[0];
    $("battery-value").textContent = number(current?.battery_v, 2);
    $("distance-value").textContent = number(current?.distance_cm);
    $("ir-left-value").textContent = logical(current?.ir_left);
    $("ir-right-value").textContent = logical(current?.ir_right);
    $("reading-time").textContent = current ? `Última lectura: ${date(current.received_at)}` : "Sin lecturas para este origen";
    const total = Number.isFinite(data.total) ? data.total : items.length;
    $("history-count").textContent = `${items.length} de ${total.toLocaleString("es-AR")} lecturas`;
    const body = $("history-body");
    const fragment = document.createDocumentFragment();
    if (!items.length) {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 6;
      cell.className = "table-empty";
      cell.textContent = "Todavía no hay lecturas para mostrar.";
      row.append(cell); fragment.append(row);
    } else {
      for (const item of items) {
        const row = document.createElement("tr");
        const values = [date(item.received_at), item.battery_v == null ? "—" : `${number(item.battery_v, 2)} V`, item.distance_cm == null ? "—" : `${number(item.distance_cm)} cm`, logical(item.ir_left), logical(item.ir_right), `${number(item.pwm_left, 0)} / ${number(item.pwm_right, 0)}`];
        for (const value of values) { const cell = document.createElement("td"); cell.textContent = value; row.append(cell); }
        fragment.append(row);
      }
    }
    body.replaceChildren(fragment);
    renderChart(items);
  }

  function renderChart(items) {
    const readings = items.slice().reverse().filter((item) => typeof item.distance_cm === "number" && Number.isFinite(item.distance_cm));
    $("chart-empty").hidden = readings.length > 0;
    $("chart-content").hidden = readings.length === 0;
    if (!readings.length) { $("chart-line").setAttribute("points", ""); return; }
    const values = readings.map((item) => item.distance_cm);
    const min = Math.min(...values), max = Math.max(...values);
    const span = max - min;
    const times = readings.map((item) => new Date(item.received_at).getTime());
    const validTimes = times.every(Number.isFinite) && times[times.length - 1] > times[0];
    const points = values.map((value, index) => {
      const x = values.length === 1 ? 400 : validTimes ? 5 + (times[index] - times[0]) / (times[times.length - 1] - times[0]) * 790 : 5 + index / (values.length - 1) * 790;
      const y = span ? 165 - (value - min) / span * 150 : 90;
      return [x, y];
    });
    $("chart-line").setAttribute("points", points.map((point) => point.join(",")).join(" "));
    $("chart-dot").setAttribute("cx", String(points[points.length - 1][0]));
    $("chart-dot").setAttribute("cy", String(points[points.length - 1][1]));
    $("chart-max").textContent = number(max);
    $("chart-min").textContent = span ? `${number(min)} cm` : `Constante: ${number(min)} cm`;
    $("chart-start").textContent = date(readings[0].received_at, true);
    $("chart-end").textContent = date(readings[readings.length - 1].received_at, true);
    $("distance-chart").setAttribute("aria-label", `${readings.length} lecturas de distancia. Mínima ${number(min)} centímetros; máxima ${number(max)} centímetros. Última ${number(values[values.length - 1])} centímetros.`);
  }

  function renderEvents(data) {
    const fragment = document.createDocumentFragment();
    if (!data.items?.length) { const empty = document.createElement("li"); empty.className = "events-empty"; empty.textContent = "La actividad aparecerá acá."; fragment.append(empty); }
    for (const event of data.items || []) {
      const item = document.createElement("li");
      const level = ["info", "warning", "error"].includes(event.level) ? event.level : "info";
      item.className = `event ${level}`;
      const dot = document.createElement("span"); dot.className = "event-dot"; dot.setAttribute("aria-hidden", "true");
      const content = document.createElement("div");
      const message = document.createElement("p"); message.className = "event-message"; message.textContent = event.message;
      const time = document.createElement("div"); time.className = "event-time"; time.textContent = date(event.created_at);
      content.append(message, time); item.append(dot, content); fragment.append(item);
    }
    $("events-list").replaceChildren(fragment);
  }

  async function poll() {
    clearTimeout(state.timer);
    if (state.polling) { state.pending = true; return; }
    state.polling = true;
    try {
      const status = await request("/api/v1/status");
      state.status = status;
      if (!state.initialized) { state.source = status.demo_running ? "demo" : "device"; state.initialized = true; }
      renderStatus();
      const source = state.source;
      const [telemetry, events] = await Promise.all([request(`/api/v1/telemetry?source=${source}&limit=60`), request("/api/v1/events?limit=10")]);
      if (source === state.source) renderTelemetry(telemetry);
      renderEvents(events);
      connection(true);
    } catch (_) { connection(false); }
    finally {
      state.polling = false;
      const delay = state.pending ? 0 : 1000;
      state.pending = false;
      state.timer = setTimeout(poll, delay);
    }
  }

  function selectSource(source) {
    if (state.source === source) return;
    state.source = source;
    state.initialized = true;
    renderSource();
    renderTelemetry({ items: [], total: 0 });
    poll();
  }

  $("source-device").addEventListener("click", () => selectSource("device"));
  $("source-demo").addEventListener("click", () => selectSource("demo"));
  $("retry-button").addEventListener("click", poll);
  $("demo-button").addEventListener("click", async () => {
    if (state.writing || !state.online || !state.status) return;
    state.writing = true;
    $("demo-button").disabled = true;
    $("action-error").hidden = true;
    const starting = !state.status.demo_running;
    try {
      const result = await request(`/api/v1/demo/${starting ? "start" : "stop"}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
      state.status.demo_running = result.running;
      if (starting) selectSource("demo");
      renderStatus();
      poll();
    } catch (_) {
      $("action-error").textContent = "No se pudo cambiar la simulación. Comprobá la conexión e intentá nuevamente.";
      $("action-error").hidden = false;
    } finally { state.writing = false; $("demo-button").disabled = !state.online; }
  });
  poll();
})();
