import React, { useState, useEffect } from 'react';
import { Mail, Lock, User, Eye, EyeOff, ArrowRight, Sparkles, ShieldCheck, LogIn, UserPlus, AlertCircle, Loader2, CheckCircle2 } from 'lucide-react';

// FIXED: Import real API instead of mock
// Adjust the path based on your project structure:
// If api.js is in src/lib/api.js, use: import { login, signup, getApiBase } from '../lib/api';
// If api.js is in src/api.js, use: import { login, signup, getApiBase } from '../api';
// If api.js is in src/utils/api.js, use: import { login, signup, getApiBase } from '../utils/api';
import { login, signup, getApiBase } from '../api';

// Export LoginPage so it can be imported individually
export function LoginPage({ onAuthed, switchToSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    // Listen for Google OAuth callback
    const handleMessage = (event) => {
      // Verify origin for security
      const expectedOrigin = new URL(getApiBase()).origin;
      if (event.origin !== expectedOrigin && event.origin !== window.location.origin) {
        console.warn('Ignored message from unexpected origin:', event.origin);
        return;
      }
      
      if (event.data?.access_token) {
        localStorage.setItem('access_token', event.data.access_token);
        setSuccess(true);
        setTimeout(() => {
          onAuthed?.('strategy'); // Pass 'strategy' for Google login too
        }, 800);
      }
    };
    
    // Also check for hash-based token (fallback method)
    const checkHash = () => {
      const hash = window.location.hash;
      if (hash.includes('access_token=')) {
        const token = hash.split('access_token=')[1].split('&')[0];
        localStorage.setItem('access_token', token);
        window.location.hash = ''; // Clear hash
        setSuccess(true);
        setTimeout(() => {
          onAuthed?.('strategy');
        }, 800);
      }
    };
    
    window.addEventListener('message', handleMessage);
    checkHash();
    
    return () => window.removeEventListener('message', handleMessage);
  }, [onAuthed]);

  const doLogin = async () => {
    if (!email || !password) {
      setNote('Please fill in all fields');
      return;
    }
    
    setLoading(true);
    setNote('');
    
    try {
      await login({ email, password });
      setSuccess(true);
      setTimeout(() => {
        onAuthed?.('strategy'); // Pass 'strategy' as the tab to navigate to
      }, 800);
    } catch (e) {
      setNote(e.response?.data?.detail || 'Login failed. Please check your credentials.');
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    const base = getApiBase();
    const authUrl = `${base}/auth/google/login`;
    
    const w = window.open(
      authUrl,
      'google-auth',
      'width=520,height=600,left=100,top=100'
    );
    
    if (!w) {
      setNote('Popup blocked. Please enable popups and try again.');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') doLogin();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-violet-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo & Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="relative">
              <div className="text-5xl animate-pulse">🧬</div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Healytics
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Welcome back! Sign in to continue</p>
        </div>

        {/* Main Card */}
        <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 p-8 transform transition-all duration-500 hover:shadow-3xl">
          {success ? (
            <div className="text-center py-12 animate-fade-in">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-emerald-100 rounded-full">
                  <CheckCircle2 className="w-16 h-16 text-emerald-600 animate-bounce" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Login Successful!</h3>
              <p className="text-gray-600">Redirecting to dashboard...</p>
            </div>
          ) : (
            <>
              {/* Header */}
              <div className="flex items-center gap-3 mb-8">
                <div className="p-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-xl shadow-lg">
                  <LogIn className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Sign In</h2>
              </div>

              {/* Google Sign In */}
              <button
                onClick={handleGoogleLogin}
                className="w-full mb-6 py-3.5 px-4 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 flex items-center justify-center gap-3 group font-semibold text-gray-700 shadow-sm hover:shadow-md"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                <span className="group-hover:translate-x-0.5 transition-transform duration-200">
                  Continue with Google
                </span>
              </button>

              {/* Divider */}
              <div className="relative mb-6">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-white text-gray-500 font-medium">Or sign in with email</span>
                </div>
              </div>

              {/* Email Input */}
              <div className="space-y-5 mb-6">
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Email Address
                  </label>
                  <div className="relative group">
                    <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type="email"
                      className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80 text-gray-800 placeholder-gray-400"
                      placeholder="you@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      onKeyPress={handleKeyPress}
                    />
                  </div>
                </div>

                {/* Password Input */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Password
                  </label>
                  <div className="relative group">
                    <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className="w-full pl-12 pr-12 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80 text-gray-800 placeholder-gray-400"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      onKeyPress={handleKeyPress}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Error Message */}
              {note && (
                <div className="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-xl flex items-start gap-3 animate-shake">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-red-700 font-medium">{note}</p>
                </div>
              )}

              {/* Sign In Button */}
              <button
                onClick={doLogin}
                disabled={loading}
                className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${
                  loading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700'
                }`}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Signing in...
                  </>
                ) : (
                  <>
                    Sign In
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
                  </>
                )}
              </button>

              {/* Sign Up Link */}
              <div className="mt-6 text-center">
                <p className="text-gray-600">
                  Don't have an account?{' '}
                  <button
                    onClick={switchToSignup}
                    className="text-violet-600 hover:text-violet-700 font-semibold hover:underline transition-colors duration-200"
                  >
                    Create one now
                  </button>
                </p>
              </div>
            </>
          )}
        </div>

        {/* Security Badge */}
        <div className="mt-6 flex items-center justify-center gap-2 text-gray-600">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          <span className="text-sm font-medium">Secure & encrypted connection</span>
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
        
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
        
        .animate-shake {
          animation: shake 0.3s ease-in-out;
        }
      `}</style>
    </div>
  );
}

function SignupPage({ onAuthed, switchToLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const doSignup = async () => {
    if (!name || !email || !password) {
      setNote('Please fill in all fields');
      return;
    }
    
    if (password.length < 6) {
      setNote('Password must be at least 6 characters');
      return;
    }
    
    setLoading(true);
    setNote('');
    
    try {
      await signup({ email, password, name });
      setSuccess(true);
      setTimeout(() => {
        onAuthed?.('strategy'); // Pass 'strategy' for signup too
      }, 800);
    } catch (e) {
      setNote(e.response?.data?.detail || 'Signup failed. Email might already be registered.');
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') doSignup();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-violet-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo & Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="relative">
              <div className="text-5xl animate-pulse">🧬</div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Healytics
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Create your account to get started</p>
        </div>

        {/* Main Card */}
        <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 p-8 transform transition-all duration-500 hover:shadow-3xl">
          {success ? (
            <div className="text-center py-12 animate-fade-in">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-emerald-100 rounded-full">
                  <CheckCircle2 className="w-16 h-16 text-emerald-600 animate-bounce" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Account Created!</h3>
              <p className="text-gray-600">Redirecting to dashboard...</p>
            </div>
          ) : (
            <>
              {/* Header */}
              <div className="flex items-center gap-3 mb-8">
                <div className="p-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-xl shadow-lg">
                  <UserPlus className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Create Account</h2>
              </div>

              {/* Form Inputs */}
              <div className="space-y-5 mb-6">
                {/* Name Input */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Full Name
                  </label>
                  <div className="relative group">
                    <User className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type="text"
                      className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80 text-gray-800 placeholder-gray-400"
                      placeholder="John Doe"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      onKeyPress={handleKeyPress}
                    />
                  </div>
                </div>

                {/* Email Input */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Email Address
                  </label>
                  <div className="relative group">
                    <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type="email"
                      className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80 text-gray-800 placeholder-gray-400"
                      placeholder="you@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      onKeyPress={handleKeyPress}
                    />
                  </div>
                </div>

                {/* Password Input */}
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700 ml-1">
                    Password
                  </label>
                  <div className="relative group">
                    <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-violet-600 transition-colors duration-200" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className="w-full pl-12 pr-12 py-3.5 border-2 border-gray-200 rounded-xl focus:border-violet-500 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80 text-gray-800 placeholder-gray-400"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      onKeyPress={handleKeyPress}
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

              {/* Error Message */}
              {note && (
                <div className="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-xl flex items-start gap-3 animate-shake">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-red-700 font-medium">{note}</p>
                </div>
              )}

              {/* Sign Up Button */}
              <button
                onClick={doSignup}
                disabled={loading}
                className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${
                  loading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700'
                }`}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Creating account...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Create Account
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
                  </>
                )}
              </button>

              {/* Login Link */}
              <div className="mt-6 text-center">
                <p className="text-gray-600">
                  Already have an account?{' '}
                  <button
                    onClick={switchToLogin}
                    className="text-violet-600 hover:text-violet-700 font-semibold hover:underline transition-colors duration-200"
                  >
                    Sign in here
                  </button>
                </p>
              </div>
            </>
          )}
        </div>

        {/* Security Badge */}
        <div className="mt-6 flex items-center justify-center gap-2 text-gray-600">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          <span className="text-sm font-medium">Secure & encrypted connection</span>
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
        
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
        
        .animate-shake {
          animation: shake 0.3s ease-in-out;
        }
      `}</style>
    </div>
  );
}
export default LoginPage;
// Demo component to show both page