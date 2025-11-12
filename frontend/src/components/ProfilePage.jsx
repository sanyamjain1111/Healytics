
import React from 'react';
import { me, updateProfile, setPassword } from '../api';

export default function ProfilePage() {
  const [user, setUser] = React.useState(null);
  const [name, setName] = React.useState('');
  const [picture, setPicture] = React.useState('');
  const [note, setNote] = React.useState('');
  const [pwd, setPwd] = React.useState('');
  const [pwdCurrent, setPwdCurrent] = React.useState('');

  React.useEffect(() => {
    (async () => {
      try {
        const u = await me();
        setUser(u);
        setName(u?.name || '');
        setPicture(u?.picture || '');
      } catch (e) {
        setNote('Failed to load profile');
      }
    })();
  }, []);

  const saveProfile = async () => {
    setNote('');
    try {
      const u = await updateProfile({ name, picture });
      setUser(prev => ({ ...prev, ...u }));
      setNote('Profile updated');
    } catch (e) {
      setNote('Failed to update profile');
    }
  };

  const savePassword = async () => {
    setNote('');
    try {
      await setPassword({ new_password: pwd, current_password: user?.has_password ? pwdCurrent : undefined });
      setNote('Password set successfully');
      setPwd(''); setPwdCurrent('');
      const u = await me(); setUser(u);
    } catch (e) {
      setNote('Failed to set password');
    }
  };

  if (!user) return <div className="max-w-3xl mx-auto p-6">Loading…</div>;

  return (
    <div className="max-w-3xl mx-auto bg-white rounded-2xl p-6 shadow">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      {(!user.has_password) && (
        <div className="mb-4 p-3 rounded bg-yellow-50 border border-yellow-200 text-yellow-800">
          You signed in with Google. Please set a password to enable email/password login.
        </div>
      )}
      <div className="grid gap-4">
        <div>
          <label className="block text-sm text-gray-600">Email</label>
          <div className="border rounded px-3 py-2 bg-gray-50">{user.email}</div>
        </div>
        <div>
          <label className="block text-sm text-gray-600">Name</label>
          <input className="w-full border rounded px-3 py-2" value={name} onChange={e=>setName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm text-gray-600">Picture URL</label>
          <input className="w-full border rounded px-3 py-2" value={picture} onChange={e=>setPicture(e.target.value)} />
        </div>
        <button className="bg-indigo-600 text-white rounded px-4 py-2" onClick={saveProfile}>Save profile</button>
      </div>
      <div className="h-px bg-gray-200 my-6" />
      <h3 className="text-xl font-semibold mb-2">{user.has_password ? 'Change password' : 'Set password'}</h3>
      <div className="grid gap-3">
        {user.has_password && (
          <input type="password" className="border rounded px-3 py-2" placeholder="Current password" value={pwdCurrent} onChange={e=>setPwdCurrent(e.target.value)} />
        )}
        <input type="password" className="border rounded px-3 py-2" placeholder="New password" value={pwd} onChange={e=>setPwd(e.target.value)} />
        <button className="bg-emerald-600 text-white rounded px-4 py-2" onClick={savePassword}>
          {user.has_password ? 'Update password' : 'Set password'}
        </button>
      </div>
      {note && <div className="mt-4 text-sm text-gray-700">{note}</div>}
    </div>
  );
}