const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

async function json(res) {
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || res.statusText);
  }
  return res.json();
}

export const api = {
  base: API_BASE,
  async get(path) { return json(await fetch(`${API_BASE}${path}`, {cache:'no-store'})); },
  async post(path, body) {
    return json(await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }));
  },
  async upload(path, formData) {
    const res = await fetch(`${API_BASE}${path}`, { method:'POST', body: formData });
    return json(res);
  }
};
