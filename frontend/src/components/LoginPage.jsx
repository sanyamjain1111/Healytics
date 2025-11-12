
import React, { useState } from 'react';
import { login } from '../api';

export default function LoginPage({ onAuthed, switchToSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [note, setNote] = useState('');

  const doLogin = async () => {
    try {
      await login({ email, password });
      onAuthed?.();
    } catch (e) {
      setNote('Login failed');
    }
  };
  const google = () => {
    const w = window.open(`${localStorage.getItem('apiBase') || 'http://127.0.0.1:8000'}/auth/google/login`, 'g', 'width=520,height=600');
    if (!w) setNote('Popup blocked; enable popups');
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-xl p-6 shadow">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <div className="space-y-3">
        <input className="w-full border rounded px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" className="w-full border rounded px-3 py-2" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="w-full bg-indigo-600 text-white py-2 rounded" onClick={doLogin}>Login</button>
        <button className="w-full border py-2 rounded" onClick={google}>Continue with Google</button>
        <div className="text-sm">
          New here? <button className="text-indigo-600" onClick={switchToSignup}>Create an account</button>
        </div>
        {note && <div className="text-rose-600 text-sm">{note}</div>}
      </div>
    </div>
  );
}