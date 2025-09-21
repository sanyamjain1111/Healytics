import axios from 'axios';

const DEFAULT_BASE = localStorage.getItem('apiBase') || 'http://127.0.0.1:8000';

export const getApiBase = () => localStorage.getItem('apiBase') || DEFAULT_BASE;
export const setApiBase = (url) => localStorage.setItem('apiBase', url);

export const api = () => axios.create({
  baseURL: getApiBase(),
  headers: { 'Content-Type': 'application/json' },
});

export async function fetchArtifact(path) {
  const base = getApiBase();
  try {
    const res = await axios.get(`${base}/artifacts/get`, { params: { path } });
    return res.data;
  } catch (e) {
    try {
      const res = await axios.get(`${base}/${path}`);
      return res.data;
    } catch (e2) {
      throw new Error(`Unable to load artifact at ${path}`);
    }
  }
}
