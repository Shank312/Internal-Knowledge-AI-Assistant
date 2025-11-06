

const API = (path) => `http://localhost:8000${path}`;

async function upload() {
  const up = document.getElementById("file");
  const out = document.getElementById("upres");
  out.textContent = "Uploading...";
  const files = Array.from(up.files || []);
  const results = [];
  for (const f of files) {
    const fd = new FormData();
    fd.append("file", f);
    const r = await fetch(API("/v1/ingest/upload"), { method: "POST", body: fd });
    const j = await r.json();
    results.push(j);
  }
  out.textContent = "Uploaded: " + JSON.stringify(results, null, 2);
}

async function ask() {
  const q = document.getElementById("q").value;
  const ans = document.getElementById("ans");
  ans.textContent = "Thinking...";
  const r = await fetch(API("/v1/chat"), {
    method: "POST",
    headers: { "Content-Type":"application/json" },
    body: JSON.stringify({ query: q })
  });
  const j = await r.json();
  ans.innerHTML = `<div class='msg'>${j.answer}</div>` +
    `<div class='cit'>Citations:<br>${(j.citations||[]).map(c => `• <b>${c.filename}</b> — ${c.snippet.replaceAll('<','&lt;')}`).join("<br>")}</div>`;
}
