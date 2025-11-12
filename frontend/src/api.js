import axios from 'axios';

const DEFAULT_BASE = localStorage.getItem('apiBase') || 'http://127.0.0.1:8000';

export const getApiBase = () => localStorage.getItem('apiBase') || DEFAULT_BASE;
export const setApiBase = (url) => localStorage.setItem('apiBase', url);

export const api = () => {
  const instance = axios.create({
    baseURL: getApiBase(),
  });
  instance.interceptors.request.use((config) => {
    const tok = localStorage.getItem('access_token');
    if (tok) config.headers['Authorization'] = `Bearer ${tok}`;
    // Set content-type only for JSON; let browser set it for FormData
    if (config.data instanceof FormData) {
      if (config.headers) delete config.headers['Content-Type'];
    } else {
      config.headers = config.headers || {};
      if (!config.headers['Content-Type']) config.headers['Content-Type'] = 'application/json';
    }
    return config;
  });
  return instance;
};

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

// --- NEW: helpers for dropdowns ---
export async function listDatasets() {
  const client = api();
  const { data } = await client.get('/datasets');
  return data.datasets || [];
}
  
export async function listCreatedStrategies(datasetId) {
  const client = api();
  const { data } = await client.get('/strategies/created', { params: { dataset_id: datasetId } });
  return data.strategies || [];
}

export async function listStrategyCatalog() {
  const client = api();
  const { data } = await client.get('/strategies');
  return data.strategies || [];
}

// Auth helpers
export async function signup({ email, password, name }) {
  const { data } = await api().post('/auth/signup', { email, password, name });
  localStorage.setItem('access_token', data.access_token);
  return data;
}

export async function login({ email, password }) {
  const { data } = await api().post('/auth/login', { email, password });
  localStorage.setItem('access_token', data.access_token);
  return data;
}
export async function me() {
  const { data } = await api().get('/auth/me');
  return data.user;
}
export async function updateProfile({ name, picture }) {
  const { data } = await api().post('/auth/update_profile', { name, picture });
  return data.user;
}
export async function setPassword({ new_password, current_password }) {
  const { data } = await api().post('/auth/set_password', { new_password, current_password });
  return data.ok;
}