import React, { useState } from 'react';
import { signup } from '../api';
export default function SignupPage({ onAuthed, switchToLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [note, setNote] = useState('');

  const doSignup = async () => {
    try {
      await signup({ email, password, name });
      onAuthed?.();
    } catch (e) {
      setNote('Signup failed (maybe user exists?)');
    }
  };
  return (
    <div className="max-w-md mx-auto bg-white rounded-xl p-6 shadow">
      <h2 className="text-xl font-bold mb-4">Create account</h2>
      <div className="space-y-3">
        <input className="w-full border rounded px-3 py-2" placeholder="Full name" value={name} onChange={e=>setName(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" className="w-full border rounded px-3 py-2" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="w-full bg-indigo-600 text-white py-2 rounded" onClick={doSignup}>Sign up</button>
        <div className="text-sm">
          Already have an account? <button className="text-indigo-600" onClick={switchToLogin}>Login</button>
        </div>
        {note && <div className="text-rose-600 text-sm">{note}</div>}
      </div>
    </div>
  );
}