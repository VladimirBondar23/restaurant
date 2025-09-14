const API_BASE = "http://localhost:8000";

function getPayload() {
  const size = parseFloat(document.getElementById("size").value || "0");
  const seats = parseInt(document.getElementById("seats").value || "0", 10);
  const features = Array.from(document.querySelectorAll(".feature:checked")).map(cb => cb.value);
  return { size_m2: size, seats, features };
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

function renderMarkdownLite(md) {
  if (!md) return "";
  return md
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/^- (.*)$/gm, "<li>$1</li>")
    .replace(/(<li>.*<\/li>)(?!\s*<li>)/gs, "<ul>$1</ul>")
    .replace(/\n{2,}/g, "<br/><br/>")
    .replace(/\n/g, "<br/>");
}

async function generateReport() {
  const statusEl = document.getElementById("status");
  const reportEl = document.getElementById("report");
  const matchedEl = document.getElementById("matched");
  const metaEl = document.getElementById("result-meta");

  statusEl.textContent = "Generating…";
  reportEl.innerHTML = "";
  matchedEl.innerHTML = "";
  metaEl.textContent = "";

  const payload = getPayload();

  try {
    const res = await fetch(`${API_BASE}/api/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const t = await res.text();
      reportEl.innerHTML = `<pre class="error">${escapeHtml(t)}</pre>`;
      statusEl.textContent = "Error";
      return;
    }

    const data = await res.json();

    metaEl.textContent = `Matched ${data.matched_count} rules: ${data.matched_ids.join(", ")}`;
    reportEl.innerHTML = renderMarkdownLite(data.report_markdown);

    const ruleItems = data.raw_rules.map(r =>
      `<li><strong>${escapeHtml(r.category)}</strong> [${escapeHtml(r.priority)}] — ${escapeHtml(r.requirement)} <em>(${escapeHtml(r.authority)})</em></li>`
    ).join("");

    matchedEl.innerHTML = `<h3>Matched Rules</h3><ul>${ruleItems}</ul>`;
    statusEl.textContent = "Done";
  } catch (err) {
    reportEl.innerHTML = `<pre class="error">${escapeHtml(String(err))}</pre>`;
    statusEl.textContent = "Error";
  }
}

document.getElementById("btn-report").addEventListener("click", generateReport);
