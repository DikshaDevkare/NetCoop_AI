import React, { useEffect, useState } from 'react';
import { AppLayout } from '../components/layout/AppLayout';
import { api } from '../services/api';
import { Link } from 'react-router-dom';
import {
  Search,
  Filter,
  Calendar,
  AlertCircle,
  CheckCircle2,
  Clock,
  ArrowRight,
  Download,
  BarChart2,
  PieChart as PieIcon
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';

export const IncidentHistory: React.FC = () => {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>({
    total_incidents: 124,
    resolved_pct: 48,
    in_progress_pct: 32,
    open_pct: 20,
  });
  const [trendHistory, setTrendHistory] = useState<any[]>([
    { date: 'Aug 1', incidents: 4 },
    { date: 'Aug 5', incidents: 7 },
    { date: 'Aug 10', incidents: 3 },
    { date: 'Aug 15', incidents: 9 },
    { date: 'Aug 20', incidents: 6 },
    { date: 'Aug 25', incidents: 11 },
    { date: 'Aug 29', incidents: 8 },
    { date: 'Aug 31', incidents: 5 },
  ]);
  const [causeDistribution, setCauseDistribution] = useState<any[]>([
    { name: 'Congestion', value: 38, color: '#FF781F' },
    { name: 'Interface failure', value: 22, color: '#FF4568' },
    { name: 'DNS/DHCP', value: 18, color: '#438BFF' },
    { name: 'Device Overload', value: 12, color: '#A855F7' },
    { name: 'Others', value: 10, color: '#20E88A' },
  ]);

  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('All Severity');

  const fetchIncidents = async () => {
    try {
      const data = await api.getIncidents({
        severity: severityFilter === 'All Severity' ? undefined : severityFilter,
        search: search || undefined,
      });
      if (data) {
        if (data.incidents) setIncidents(data.incidents);
        if (data.metrics) setMetrics(data.metrics);
        if (data.trend_history) setTrendHistory(data.trend_history);
        if (data.root_cause_distribution) setCauseDistribution(data.root_cause_distribution);
      }
    } catch (err) {
      console.warn('Using baseline history records:', err);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, [severityFilter, search]);

  return (
    <AppLayout
      title="Incident History"
      subtitle="Search, filter and analyze past network incidents."
    >
      {/* 4 Metrics Header Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* Total Incidents */}
        <div className="glass-panel rounded-2xl p-4">
          <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">Total Incidents</p>
          <h2 className="text-3xl font-extrabold text-white mt-1">{metrics.total_incidents}</h2>
        </div>
        {/* Resolved % */}
        <div className="glass-panel rounded-2xl p-4 border-l-4 border-l-[#20E88A]">
          <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">Resolved</p>
          <h2 className="text-3xl font-extrabold text-[#20E88A] mt-1">{metrics.resolved_pct}%</h2>
        </div>
        {/* In Progress % */}
        <div className="glass-panel rounded-2xl p-4 border-l-4 border-l-[#A855F7]">
          <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">In Progress</p>
          <h2 className="text-3xl font-extrabold text-[#A855F7] mt-1">{metrics.in_progress_pct}%</h2>
        </div>
        {/* Open % */}
        <div className="glass-panel rounded-2xl p-4 border-l-4 border-l-[#FF781F]">
          <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">Open</p>
          <h2 className="text-3xl font-extrabold text-[#FF781F] mt-1">{metrics.open_pct}%</h2>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-panel rounded-2xl p-3 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3">
          {/* Severity Dropdown */}
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="bg-[#140e26] border border-[#2b1f44] text-xs text-white rounded-xl px-3 py-1.5 focus:outline-none focus:border-[#FF781F]"
          >
            <option>All Severity</option>
            <option>Critical</option>
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>

          {/* Date Range Badge */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#140e26] border border-[#2b1f44] text-xs text-[#A9A3B8]">
            <Calendar className="w-3.5 h-3.5 text-[#FF781F]" />
            <span>Aug 1, 2025 - Aug 31, 2025</span>
          </div>
        </div>

        {/* Search Input */}
        <div className="relative w-64">
          <Search className="w-3.5 h-3.5 text-[#8b82a0] absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by ID, root cause..."
            className="w-full bg-[#140e26] border border-[#2b1f44] text-xs text-white rounded-xl pl-8 pr-3 py-1.5 focus:outline-none focus:border-[#FF781F]"
          />
        </div>
      </div>

      {/* Charts Row: Trend Line & Donut Root Cause Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Chart 1: Incident Trend (Last 30 Days) */}
        <div className="glass-panel rounded-2xl p-4">
          <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2">Incident Trend (Last 30 Days)</h4>
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendHistory}>
                <defs>
                  <linearGradient id="purpleGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#A855F7" stopOpacity={0.6} />
                    <stop offset="95%" stopColor="#A855F7" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#7e7496" fontSize={10} />
                <YAxis stroke="#7e7496" fontSize={10} />
                <Tooltip contentStyle={{ background: '#120c22', borderColor: '#A855F7', fontSize: 10 }} />
                <Area type="monotone" dataKey="incidents" stroke="#A855F7" strokeWidth={2} fill="url(#purpleGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Root Cause Distribution Donut */}
        <div className="glass-panel rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3">Root Cause Distribution</h4>
            <div className="space-y-1.5 text-xs">
              {causeDistribution.map((item, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-[#A9A3B8] text-[11px]">{item.name}</span>
                  <span className="font-mono font-bold text-white text-[11px] ml-auto">{item.value}%</span>
                </div>
              ))}
            </div>
          </div>
          <div className="w-36 h-36 shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={causeDistribution}
                  dataKey="value"
                  innerRadius={36}
                  outerRadius={56}
                  paddingAngle={4}
                >
                  {causeDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: '#120c22', borderColor: '#FF781F', fontSize: 10 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Incidents Table */}
      <div className="glass-panel rounded-2xl p-4 overflow-hidden">
        <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3">Historical Incident Logs</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#2a1e42] text-[#8e85a4] uppercase text-[10px] tracking-wider">
                <th className="pb-2 pl-2">ID</th>
                <th className="pb-2">Root Cause</th>
                <th className="pb-2">Severity</th>
                <th className="pb-2">Status</th>
                <th className="pb-2">Occurred At</th>
                <th className="pb-2 pr-2 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#221736]">
              {incidents.map((inc) => (
                <tr key={inc.id} className="hover:bg-[#1a122e]/60 transition-colors">
                  <td className="py-3 pl-2 font-mono font-bold text-[#FF781F]">{inc.id}</td>
                  <td className="py-3 font-medium text-white max-w-xs truncate">{inc.root_cause}</td>
                  <td className="py-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        inc.severity === 'Critical'
                          ? 'bg-[#FF4568]/20 text-[#FF4568]'
                          : inc.severity === 'High'
                          ? 'bg-[#FF781F]/20 text-[#FF781F]'
                          : 'bg-[#FFC247]/20 text-[#FFC247]'
                      }`}
                    >
                      {inc.severity}
                    </span>
                  </td>
                  <td className="py-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        inc.status === 'Resolved'
                          ? 'bg-[#20E88A]/20 text-[#20E88A]'
                          : 'bg-[#A855F7]/20 text-[#A855F7]'
                      }`}
                    >
                      {inc.status}
                    </span>
                  </td>
                  <td className="py-3 text-[#A9A3B8] font-mono text-[11px]">{inc.occurred_at}</td>
                  <td className="py-3 pr-2 text-right">
                    <Link
                      to={`/incidents/${inc.id}`}
                      className="px-2.5 py-1 rounded bg-[#201538] hover:bg-[#FF781F] hover:text-white text-[11px] text-[#A9A3B8] transition-all inline-block"
                    >
                      Inspect
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppLayout>
  );
};
