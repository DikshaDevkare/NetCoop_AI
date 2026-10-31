import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LivingBackground } from '../components/layout/LivingBackground';
import { api } from '../services/api';
import { Zap, User, Mail, Lock, Building, ShieldCheck, ArrowRight, Loader2, AlertCircle } from 'lucide-react';

export const SignupPage: React.FC = () => {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [organization, setOrganization] = useState('Campus Network Operations');
  const [role, setRole] = useState('Network Engineer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password) {
      setError('Please fill in all required fields.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      await api.register({ name, email, password, organization, role });
      navigate('/dashboard');
    } catch (err: any) {
      console.warn('Signup error:', err);
      setError(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#070711] text-[#F5F2FA] flex items-center justify-center p-4">
      <LivingBackground />

      <div className="relative z-10 w-full max-w-md glass-panel rounded-3xl p-8 border border-[#2b1f44] shadow-2xl">
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#FF781F] to-[#A855F7] p-0.5 mx-auto mb-3 shadow-lg shadow-orange-500/30 flex items-center justify-center">
            <div className="w-full h-full bg-[#120c22] rounded-[14px] flex items-center justify-center">
              <Zap className="w-6 h-6 text-[#FF781F]" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-white tracking-wide">Create Operator Account</h2>
          <p className="text-xs text-[#A9A3B8] mt-1">Join the NetCoop AI Diagnostic Mesh</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-[#2b0e18] border border-[#FF4568]/40 text-[#FF4568] text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSignup} className="space-y-3.5">
          <div>
            <label className="text-xs font-semibold text-[#A9A3B8] block mb-1">Full Name</label>
            <div className="relative">
              <User className="w-4 h-4 text-[#7d7494] absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Dr. Alex Rivera"
                className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl pl-9 pr-4 py-2 text-xs text-white focus:outline-none focus:border-[#FF781F]"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-[#A9A3B8] block mb-1">Campus Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-[#7d7494] absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex.rivera@campus.edu"
                className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl pl-9 pr-4 py-2 text-xs text-white focus:outline-none focus:border-[#FF781F]"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-semibold text-[#A9A3B8] block mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#FF781F]"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-[#A9A3B8] block mb-1">Confirm</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#FF781F]"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-[#A9A3B8] block mb-1">Organization / Campus</label>
            <input
              type="text"
              value={organization}
              onChange={(e) => setOrganization(e.target.value)}
              className="w-full bg-[#120a22] border border-[#2c2047] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#FF781F]"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 mt-2 rounded-xl bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white font-bold text-xs shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:scale-[1.01] transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <span>Create Account</span>}
          </button>
        </form>

        <div className="mt-4 text-center text-xs text-[#A9A3B8]">
          Already registered?{' '}
          <Link to="/login" className="text-[#FF781F] font-bold hover:underline">
            Sign In here
          </Link>
        </div>
      </div>
    </div>
  );
};
