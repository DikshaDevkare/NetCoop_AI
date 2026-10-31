import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LivingBackground } from '../components/layout/LivingBackground';
import { api } from '../services/api';
import { Zap, Lock, Mail, Eye, EyeOff, ArrowRight, Loader2, AlertCircle } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please fill in both email and password.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      await api.login({ email, password });
      navigate('/dashboard');
    } catch (err: any) {
      console.warn('Login error:', err);
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = () => {
    setEmail('admin@campus.edu');
    setPassword('NetCoop2026!');
  };

  return (
    <div className="relative min-h-screen bg-[#070711] text-[#F5F2FA] flex items-center justify-center p-4">
      <LivingBackground />

      <div className="relative z-10 w-full max-w-md glass-panel rounded-3xl p-8 border border-[#2b1f44] shadow-2xl">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#FF781F] to-[#A855F7] p-0.5 mx-auto mb-3 shadow-lg shadow-orange-500/30 flex items-center justify-center">
            <div className="w-full h-full bg-[#120c22] rounded-[14px] flex items-center justify-center">
              <Zap className="w-6 h-6 text-[#FF781F]" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-white tracking-wide">NetCoop AI</h2>
          <p className="text-xs text-[#A9A3B8] mt-1">Multi-Agent Network Command Centre</p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-[#2b0e18] border border-[#FF4568]/40 text-[#FF4568] text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          {/* Email */}
          <div>
            <label className="text-xs font-semibold text-[#A9A3B8] block mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-[#7d7494] absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@campus.edu"
                className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl pl-9 pr-4 py-2 text-xs text-white placeholder-[#685e7a] focus:outline-none focus:border-[#FF781F]"
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="text-xs font-semibold text-[#A9A3B8]">Password</label>
              <a href="#" className="text-[10px] text-[#FF781F] hover:underline">Forgot?</a>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#7d7494] absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl pl-9 pr-10 py-2 text-xs text-white placeholder-[#685e7a] focus:outline-none focus:border-[#FF781F]"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#7d7494] hover:text-white"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white font-bold text-xs shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:scale-[1.01] transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <span>Sign In to Command Centre</span>}
          </button>
        </form>

        {/* Demo Credentials Quick-Fill Pill */}
        <div className="mt-4 pt-4 border-t border-[#261d3b] text-center">
          <button
            type="button"
            onClick={handleQuickDemo}
            className="text-[11px] text-[#A855F7] hover:text-white font-semibold underline cursor-pointer"
          >
            ⚡ Click to Fill Demo Administrator Credentials
          </button>
        </div>

        {/* Navigation to Signup */}
        <div className="mt-4 text-center text-xs text-[#A9A3B8]">
          Don't have an operator account?{' '}
          <Link to="/signup" className="text-[#FF781F] font-bold hover:underline">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
};
