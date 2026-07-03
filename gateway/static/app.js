const TOKEN_KEY = "ems_token";
const USER_KEY  = "ems_user";
const tok = () => localStorage.getItem(TOKEN_KEY);
const usr = () => JSON.parse(localStorage.getItem(USER_KEY) || "null");

async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (tok()) headers.Authorization = `Bearer ${tok()}`;
  const r = await fetch(path, { ...opts, headers });
  const text = await r.text();
  const data = text ? JSON.parse(text) : null;
  if (!r.ok) throw new Error(data?.error || r.statusText);
  return data;
}

// ---- auth view ----
document.querySelectorAll("#authTabs a").forEach(a => a.onclick = e => {
  e.preventDefault();
  document.querySelectorAll("#authTabs a").forEach(x => x.classList.remove("active"));
  a.classList.add("active");
  const t = a.dataset.tab;
  signinForm.classList.toggle("d-none", t !== "signin");
  signupForm.classList.toggle("d-none", t !== "signup");
  authMsg.textContent = "";
});

signinForm.onsubmit = async e => {
  e.preventDefault();
  authMsg.textContent = "";
  try {
    const f = Object.fromEntries(new FormData(e.target));
    const { token, user } = await api("/auth/login", { method: "POST", body: JSON.stringify(f) });
    localStorage.setItem(TOKEN_KEY, token); localStorage.setItem(USER_KEY, JSON.stringify(user));
    boot();
  } catch (err) { authMsg.textContent = err.message; }
};

signupForm.onsubmit = async e => {
  e.preventDefault();
  authMsg.textContent = "";
  try {
    const f = Object.fromEntries(new FormData(e.target));
    const { token, user } = await api("/auth/register", { method: "POST", body: JSON.stringify(f) });
    localStorage.setItem(TOKEN_KEY, token); localStorage.setItem(USER_KEY, JSON.stringify(user));
    boot();
  } catch (err) { authMsg.textContent = err.message; }
};

logoutBtn.onclick = () => { localStorage.clear(); boot(); };

// ---- tabs ----
document.querySelectorAll("#mainTabs a").forEach(a => a.onclick = e => {
  e.preventDefault();
  document.querySelectorAll("#mainTabs a").forEach(x => x.classList.remove("active"));
  a.classList.add("active");
  const v = a.dataset.view;
  employeesView.classList.toggle("d-none", v !== "employees");
  adminView.classList.toggle("d-none", v !== "admin");
  if (v === "admin") loadUsers();
});

// ---- boot ----
async function boot() {
  const u = usr();
  if (!tok() || !u) {
    loginView.classList.remove("d-none"); appView.classList.add("d-none"); return;
  }
  loginView.classList.add("d-none"); appView.classList.remove("d-none");
  whoami.textContent = u.email;
  const isAdmin = u.role === "admin";
  roleBadge.classList.toggle("d-none", !isAdmin);
  document.querySelectorAll(".admin-only").forEach(el => el.classList.toggle("d-none", !isAdmin));
  await Promise.all([loadStats(), loadEmployees()]);
}

async function loadStats() {
  try {
    const s = await api("/dashboard/stats");
    statsRow.innerHTML = `
      ${statCard("people-fill", "Total Employees", s.total_employees)}
      ${statCard("building",     "Departments",     s.departments)}
      ${statCard("cash-stack",   "Avg. Salary",     s.avg_salary ? "$" + Math.round(s.avg_salary).toLocaleString() : "—")}
      ${statCard("person-badge", "Users",           s.total_users)}
    `;
  } catch (e) { statsRow.innerHTML = `<div class="col text-danger small">Stats unavailable: ${e.message}</div>`; }
}
const statCard = (icon, label, value) => `
  <div class="col-6 col-md-3"><div class="card p-3"><div class="d-flex align-items-center gap-3">
    <div class="rounded bg-primary-subtle text-primary p-2"><i class="bi bi-${icon} fs-4"></i></div>
    <div><div class="text-muted small">${label}</div><div class="fs-4 fw-semibold">${value}</div></div>
  </div></div></div>`;

// ---- employees ----
let empCache = [];
async function loadEmployees() {
  try { empCache = await api("/employees"); renderEmployees(empCache); }
  catch (e) { empBody.innerHTML = `<tr><td colspan="7" class="text-danger">${e.message}</td></tr>`; }
}
searchInput.oninput = () => {
  const q = searchInput.value.trim().toLowerCase();
  if (!q) return renderEmployees(empCache);
  renderEmployees(empCache.filter(e => [e.full_name,e.email,e.position,e.department].filter(Boolean).some(v => v.toLowerCase().includes(q))));
};

function renderEmployees(list) {
  const isAdmin = usr()?.role === "admin";
  if (!list.length) { empBody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No employees.</td></tr>`; return; }
  empBody.innerHTML = list.map(e => `
    <tr>
      <td>${esc(e.full_name)}</td><td>${esc(e.email)}</td>
      <td>${esc(e.position)||"—"}</td><td>${esc(e.department)||"—"}</td>
      <td>${e.salary ? "$"+Number(e.salary).toLocaleString() : "—"}</td>
      <td>${e.hire_date||"—"}</td>
      ${isAdmin ? `<td class="text-end">
        <button class="btn btn-sm btn-outline-secondary" onclick='editEmp(${e.id})'><i class="bi bi-pencil"></i></button>
        <button class="btn btn-sm btn-outline-danger" onclick='delEmp(${e.id})'><i class="bi bi-trash"></i></button>
      </td>` : ""}
    </tr>`).join("");
}
const esc = s => (s??"").toString().replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

addEmpBtn.onclick = () => {
  empForm.reset(); empForm.id.value = ""; empModalTitle.textContent = "Add employee";
};
window.editEmp = id => {
  const e = empCache.find(x => x.id === id); if (!e) return;
  for (const [k, v] of Object.entries(e)) if (empForm[k]) empForm[k].value = v ?? "";
  empModalTitle.textContent = "Update employee";
  new bootstrap.Modal(empModal).show();
};
window.delEmp = async id => {
  if (!confirm("Delete this employee?")) return;
  try { await api(`/employees/${id}`, { method: "DELETE" }); await loadEmployees(); await loadStats(); }
  catch (e) { alert(e.message); }
};
empForm.onsubmit = async e => {
  e.preventDefault();
  const f = Object.fromEntries(new FormData(e.target));
  const id = f.id; delete f.id;
  ["phone","position","department","hire_date"].forEach(k => { if (!f[k]) f[k] = null; });
  f.salary = f.salary === "" ? null : Number(f.salary);
  try {
    if (id) await api(`/employees/${id}`, { method: "PUT", body: JSON.stringify(f) });
    else    await api("/employees",       { method: "POST", body: JSON.stringify(f) });
    bootstrap.Modal.getInstance(empModal).hide();
    await loadEmployees(); await loadStats();
  } catch (err) { alert(err.message); }
};

// ---- admin ----
async function loadUsers() {
  try {
    const users = await api("/admin/users");
    userBody.innerHTML = users.map(u => `
      <tr>
        <td>${esc(u.email)}</td><td>${esc(u.full_name)||"—"}</td>
        <td><span class="badge text-bg-${u.role==='admin'?'primary':'secondary'}">${u.role}</span></td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-secondary" onclick="toggleRole(${u.id},'${u.role==='admin'?'user':'admin'}')">Make ${u.role==='admin'?'user':'admin'}</button>
          <button class="btn btn-sm btn-outline-danger" onclick="delUser(${u.id})"><i class="bi bi-trash"></i></button>
        </td>
      </tr>`).join("");
  } catch (e) { userBody.innerHTML = `<tr><td colspan="4" class="text-danger">${e.message}</td></tr>`; }
}
window.toggleRole = async (id, role) => {
  try { await api(`/admin/users/${id}/role`, { method: "POST", body: JSON.stringify({ role }) }); loadUsers(); }
  catch (e) { alert(e.message); }
};
window.delUser = async id => {
  if (!confirm("Delete this user?")) return;
  try { await api(`/admin/users/${id}`, { method: "DELETE" }); loadUsers(); loadStats(); }
  catch (e) { alert(e.message); }
};

boot();
