import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Compass,
  AlertTriangle,
  Cpu,
  FileCheck2,
  History,
  Layers,
  Activity,
  Zap,
  Radio
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'New Diagnosis', path: '/new-diagnosis', icon: Compass },
  { name: 'Incident Details', path: '/incidents/INC-1024', icon: AlertTriangle },
  { name: 'Agent Monitor', path: '/agent-monitor', icon: Cpu },
  { name: 'Diagnosis Report', path: '/diagnosis-report/INC-1024', icon: FileCheck2 },
  { name: 'Incident History', path: '/incident-history', icon: History },
  { name: 'Interop Lab', path: '/interoperability-lab', icon: Layers },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <aside className="w-64 min-h-screen bg-[#0d091a]/95 border-r border-[#261d3b] flex flex-col justify-between p-4 z-20 shrink-0 backdrop-blur-xl">
      <div>
        {/* Brand Header */}
        <NavLink to="/" className="flex items-center gap-3 px-3 py-4 mb-6 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#FF781F] via-[#FF9B35] to-[#A855F7] p-0.5 flex items-center justify-center shadow-lg shadow-orange-500/20 group-hover:shadow-orange-500/40 transition-all">
            <div className="w-full h-full bg-[#120c22] rounded-[10px] flex items-center justify-center">
              <Zap className="w-5 h-5 text-[#FF781F] group-hover:scale-110 transition-transform" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-lg tracking-wider text-white">NetCoop</span>
              <span className="font-bold text-xs px-1.5 py-0.5 rounded bg-[#FF781F]/20 text-[#FF781F] border border-[#FF781F]/40">AI</span>
            </div>
            <p className="text-[10px] text-[#A9A3B8] tracking-widest uppercase">Multi-Agent Ops</p>
          </div>
        </NavLink>

        {/* Navigation Items */}
        <nav className="space-y-1.5">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            // Check active state
            const isActive = location.pathname === item.path ||
              (item.path.startsWith('/incidents') && location.pathname.startsWith('/incidents')) ||
              (item.path.startsWith('/diagnosis-report') && location.pathname.startsWith('/diagnosis-report'));

            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={`flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all relative ${
                  isActive
                    ? 'bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white shadow-lg shadow-orange-500/30'
                    : 'text-[#A9A3B8] hover:text-white hover:bg-[#1a142c]/70'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-[#8b82a0]'}`} />
                <span>{item.name}</span>
                {isActive && (
                  <span className="absolute right-2 w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Bottom Status Pill */}
      <div className="pt-4 border-t border-[#261d3b]/70">
        <div className="flex items-center justify-between px-3 py-2.5 rounded-xl bg-[#140e26] border border-[#261d3b]">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#20E88A] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#20E88A]"></span>
            </span>
            <span className="text-[11px] font-medium text-[#20E88A]">System Online</span>
          </div>
          <span className="text-[10px] text-[#A9A3B8] font-mono">v1.0-LIVE</span>
        </div>
      </div>
    </aside>
  );
};
