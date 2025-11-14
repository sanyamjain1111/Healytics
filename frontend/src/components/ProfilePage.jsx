import React, { useState, useEffect } from 'react';
import { User, Mail, Lock, Image, Save, Camera, Shield, CheckCircle2, AlertCircle, Eye, EyeOff, Loader2, AlertTriangle, Key } from 'lucide-react';
import { me, updateProfile, setPassword } from '../api';

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [name, setName] = useState('');
  const [picture, setPicture] = useState('');
  const [note, setNote] = useState('');
  const [noteType, setNoteType] = useState('info'); // info, success, error, warning
  const [pwd, setPwd] = useState('');
  const [pwdCurrent, setPwdCurrent] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [loadingPassword, setLoadingPassword] = useState(false);
  const [imagePreview, setImagePreview] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const u = await me();
        console.log('User data loaded:', u);
        setUser(u);
        setName(u?.name || '');
        setPicture(u?.picture || '');
        setImagePreview(u?.picture || '');
        console.log('Profile picture URL:', u?.picture);
      } catch (e) {
        console.error('Failed to load user:', e);
        setNoteType('error');
        setNote('You are not logged in. Please login to view your profile.');
        setUser({ email: '', has_password: false, name: '', picture: '' });
      }
    })();
  }, []);

  const saveProfile = async () => {
    setNote('');
    setLoadingProfile(true);
    
    try {
      const u = await updateProfile({ name, picture });
      setUser(prev => ({ ...prev, ...u }));
      setImagePreview(picture);
      setNoteType('success');
      setNote('Profile updated successfully!');
      setTimeout(() => setNote(''), 3000);
    } catch (e) {
      setNoteType('error');
      setNote('Failed to update profile. Please try again.');
    } finally {
      setLoadingProfile(false);
    }
  };

  const savePassword = async () => {
    if (!pwd) {
      setNoteType('error');
      setNote('Please enter a new password');
      return;
    }
    
    if (pwd.length < 6) {
      setNoteType('error');
      setNote('Password must be at least 6 characters');
      return;
    }

    setNote('');
    setLoadingPassword(true);
    
    try {
      await setPassword({ 
        new_password: pwd, 
        current_password: user?.has_password ? pwdCurrent : undefined 
      });
      setNoteType('success');
      setNote('Password updated successfully!');
      setPwd(''); 
      setPwdCurrent('');
      const u = await me(); 
      setUser(u);
      setTimeout(() => setNote(''), 3000);
    } catch (e) {
      setNoteType('error');
      setNote('Failed to update password. Please check your current password.');
    } finally {
      setLoadingPassword(false);
    }
  };

  const handleImageUrlChange = (e) => {
    const url = e.target.value;
    setPicture(url);
    if (url) {
      setImagePreview(url);
    }
  };

  const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-violet-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600 text-lg">Loading profile...</p>
        </div>
      </div>
    );
  }

  const NotificationBanner = () => {
    if (!note) return null;
    
    const styles = {
      success: {
        bg: 'bg-emerald-50',
        border: 'border-emerald-200',
        text: 'text-emerald-700',
        icon: <CheckCircle2 className="w-5 h-5 text-emerald-600" />
      },
      error: {
        bg: 'bg-red-50',
        border: 'border-red-200',
        text: 'text-red-700',
        icon: <AlertCircle className="w-5 h-5 text-red-600" />
      },
      warning: {
        bg: 'bg-yellow-50',
        border: 'border-yellow-200',
        text: 'text-yellow-800',
        icon: <AlertTriangle className="w-5 h-5 text-yellow-600" />
      },
      info: {
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-700',
        icon: <AlertCircle className="w-5 h-5 text-blue-600" />
      }
    };

    const style = styles[noteType] || styles.info;

    return (
      <div className={`${style.bg} border-2 ${style.border} rounded-2xl p-4 flex items-start gap-3 animate-slide-down`}>
        {style.icon}
        <div className="flex-1">
          <p className={`${style.text} font-medium`}>{note}</p>
          {note.includes('not logged in') && (
            <a 
              className="text-violet-600 underline font-semibold mt-2 inline-block hover:text-violet-700 transition-colors duration-200" 
              href="#" 
              onClick={() => { 
                localStorage.removeItem('access_token'); 
                window.location.hash=''; 
                window.location.reload(); 
              }}
            >
              Go to Login →
            </a>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="relative">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl shadow-lg">
              <User className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              My Profile
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Manage your account settings and preferences</p>
        </div>

        {/* Notification Banner */}
        {note && (
          <div className="mb-6">
            <NotificationBanner />
          </div>
        )}

        {/* Warning for Google users without password */}
        {user && user.email && !user.has_password && (
          <div className="mb-6 bg-gradient-to-r from-amber-50 to-yellow-50 border-2 border-amber-200 rounded-2xl p-5 flex items-start gap-4 shadow-md animate-fade-in">
            <div className="p-2 bg-amber-100 rounded-xl">
              <Shield className="w-6 h-6 text-amber-600" />
            </div>
            <div>
              <h3 className="font-bold text-amber-900 mb-1">Secure Your Account</h3>
              <p className="text-amber-800 text-sm">
                You signed in with Google. Set a password below to enable email/password login and add an extra layer of security.
              </p>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Profile Picture Card */}
          <div className="lg:col-span-1">
            <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl">
                  <Camera className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-xl font-bold text-gray-800">Profile Photo</h2>
              </div>

              {/* Profile Image Preview */}
              <div className="mb-6">
                <div className="relative w-48 h-48 mx-auto mb-4">
                  {imagePreview && (
                    <img 
                      src={imagePreview} 
                      alt="Profile" 
                      className="w-full h-full rounded-full object-cover border-4 border-violet-200 shadow-lg"
                      onError={(e) => {
                        console.error('Image failed to load:', imagePreview);
                        e.target.style.display = 'none';
                        const fallback = e.target.nextElementSibling;
                        if (fallback) fallback.style.display = 'flex';
                      }}
                      onLoad={(e) => {
                        console.log('Image loaded successfully:', imagePreview);
                        e.target.style.display = 'block';
                        const fallback = e.target.nextElementSibling;
                        if (fallback) fallback.style.display = 'none';
                      }}
                    />
                  )}
                  <div 
                    className={`w-full h-full rounded-full bg-gradient-to-br from-violet-400 to-indigo-500 items-center justify-center text-white text-4xl font-bold shadow-lg ${imagePreview ? 'hidden' : 'flex'}`}
                    style={{ display: imagePreview ? 'none' : 'flex' }}
                  >
                    {getInitials(name || user.name)}
                  </div>
                  <div className="absolute bottom-2 right-2 p-2 bg-white rounded-full shadow-lg border-2 border-violet-200">
                    <Camera className="w-5 h-5 text-violet-600" />
                  </div>
                </div>
                <p className="text-center text-sm text-gray-600 font-semibold">
                  {name || user.name || 'Your Name'}
                </p>
                <p className="text-center text-xs text-gray-500 mt-1">
                  {user.email}
                </p>
              </div>
            </div>
          </div>

          {/* Profile Info Card */}
          <div className="lg:col-span-2">
            <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
                  <User className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-xl font-bold text-gray-800">Personal Information</h2>
              </div>

              <div className="space-y-5">
                {/* Email (Read-only) */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <div className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl bg-gray-50 text-gray-600 font-medium">
                      {user.email}
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 ml-1">Email cannot be changed</p>
                </div>

                {/* Name */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Full Name
                  </label>
                  <div className="relative group">
                    <User className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type="text"
                      className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white text-gray-800"
                      value={name}
                      onChange={e => setName(e.target.value)}
                      placeholder="Enter your full name"
                    />
                  </div>
                </div>

                {/* Picture URL */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Profile Picture URL
                  </label>
                  <div className="relative group">
                    <Image className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type="url"
                      className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white text-gray-800"
                      value={picture}
                      onChange={handleImageUrlChange}
                      placeholder="https://example.com/avatar.jpg"
                    />
                  </div>
                  <p className="text-xs text-gray-500 ml-1">Enter a URL to your profile picture</p>
                </div>

                {/* Save Profile Button */}
                <button
                  onClick={saveProfile}
                  disabled={loadingProfile}
                  className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${
                    loadingProfile
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700'
                  }`}
                >
                  {loadingProfile ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      Save Profile
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Password Section */}
        <div className="mt-6">
          <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-gradient-to-r from-rose-500 to-pink-500 rounded-xl">
                <Key className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-800">
                  {user.has_password ? 'Change Password' : 'Set Password'}
                </h2>
                <p className="text-sm text-gray-600">
                  {user.has_password 
                    ? 'Update your password to keep your account secure' 
                    : 'Create a password to enable email/password login'}
                </p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-5">
              {/* Current Password (if has password) */}
              {user.has_password && (
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Current Password
                  </label>
                  <div className="relative group">
                    <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-rose-600 transition-colors duration-200" />
                    <input
                      type={showCurrentPassword ? 'text' : 'password'}
                      className="w-full pl-12 pr-12 py-3.5 border-2 border-gray-200 rounded-xl focus:border-rose-500 focus:ring-4 focus:ring-rose-100 transition-all duration-200 bg-white text-gray-800"
                      value={pwdCurrent}
                      onChange={e => setPwdCurrent(e.target.value)}
                      placeholder="Enter current password"
                    />
                    <button
                      type="button"
                      onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                      className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                    >
                      {showCurrentPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>
              )}

              {/* New Password */}
              <div className={`space-y-2 ${!user.has_password ? 'md:col-span-2' : ''}`}>
                <label className="block text-sm font-semibold text-gray-700 ml-1">
                  New Password
                </label>
                <div className="relative group">
                  <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-rose-600 transition-colors duration-200" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    className="w-full pl-12 pr-12 py-3.5 border-2 border-gray-200 rounded-xl focus:border-rose-500 focus:ring-4 focus:ring-rose-100 transition-all duration-200 bg-white text-gray-800"
                    value={pwd}
                    onChange={e => setPwd(e.target.value)}
                    placeholder="Enter new password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                <p className="text-xs text-gray-500 ml-1">At least 6 characters</p>
              </div>
            </div>

            {/* Update Password Button */}
            <button
              onClick={savePassword}
              disabled={loadingPassword}
              className={`w-full mt-6 py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${
                loadingPassword
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-rose-600 to-pink-600 hover:from-rose-700 hover:to-pink-700'
              }`}
            >
              {loadingPassword ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Updating...
                </>
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  {user.has_password ? 'Update Password' : 'Set Password'}
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes slide-down {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
        
        .animate-slide-down {
          animation: slide-down 0.3s ease-out;
        }
      `}</style>
    </div>
  );
}