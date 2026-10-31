import React, { useState } from 'react';
import { Search, Bell, Sparkles, User, LogOut } from 'lucide-react';
import { api } from '../../services/api';
import { useNavigate } from 'react-router-dom';

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle }) => {
  const [search, setSearch] = useState('');
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const user = api.getCurrentUser() || { name: 'Dr. Sarah Connor', role: 'Chief Network Architect' };
  const navigate = useNavigate();

  const handleLogout = () => {
    api.logout();
    navigate('/login');
  };

  return (
    <header className="h-16 border-b border-[#261d3b] bg-[#0a0716]/80 backdrop-blur-xl px-6 flex items-center justify-between z-10 shrink-0">
      <div>
        {title && <h1 className="text-lg font-bold text-white tracking-wide">{title}</h1>}
        {subtitle && <p className="text-xs text-[#A9A3B8]">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        {/* Search Bar */}
        <div className="relative w-64 hidden sm:block">
          <Search className="w-4 h-4 text-[#8b82a0] absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search network, device..."
            className="w-full bg-[#150f29] border border-[#2a2042] rounded-xl pl-9 pr-4 py-1.5 text-xs text-white placeholder-[#786f8a] focus:outline-none focus:border-[#FF781F] transition-all"
          />
        </div>

        {/* Simulation Mode Pill */}
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#A855F7]/15 border border-[#A855F7]/30 text-[#A855F7] text-[11px] font-semibold">
          <Sparkles className="w-3 h-3 text-[#A855F7] animate-pulse" />
          <span>Simulation Active</span>
        </div>

        {/* Notification Bell */}
        <button className="relative p-2 rounded-xl bg-[#150f29] border border-[#2a2042] hover:border-[#FF781F]/50 text-[#A9A3B8] hover:text-white transition-all">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#FF4568] ring-2 ring-[#0a0716]"></span>
        </button>

        {/* Profile Avatar */}
        <div className="relative">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="flex items-center gap-2.5 p-1 rounded-xl hover:bg-[#150f29] transition-all border border-transparent hover:border-[#2a2042]"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#FF781F] to-[#A855F7] p-0.5 shadow-md shadow-orange-500/20">
              <div className="w-full h-full bg-[#150f29] rounded-[6px] flex items-center justify-center text-xs font-bold text-white">
                {user.name.charAt(0)}
              </div>
            </div>
            <div className="hidden lg:block text-left text-xs">
              <p className="font-semibold text-white leading-none">{user.name}</p>
              <p className="text-[10px] text-[#A9A3B8] leading-none mt-1">{user.role}</p>
            </div>
          </button>

          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-48 rounded-xl bg-[#150f29] border border-[#2a2042] shadow-2xl p-2 z-50">
              <div className="px-3 py-2 border-b border-[#2a2042]/70 text-xs text-[#A9A3B8]">
                Signed in as <span className="font-bold text-white block truncate">{user.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-2 px-3 py-2 mt-1 text-xs text-[#FF4568] hover:bg-[#FF4568]/10 rounded-lg transition-all"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Sign Out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
