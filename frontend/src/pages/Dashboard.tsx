import React, { useEffect, useState } from 'react';
import { AppLayout } from '../components/layout/AppLayout';
import { Topology3D } from '../components/network/Topology3D';
import { ConfidenceGauge } from '../components/common/ConfidenceGauge';
import { api } from '../services/api';
import {
  Activity,
  Cpu,
  Server,
  AlertTriangle,
  RefreshCw,
  TrendingUp,
  Zap,
  ArrowRight
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { Link } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>({
    network_health_pct: 93,
    ai_agents_online: 5,
    active_devices: 428,
    open_incidents: 1,
  });

  const [telemetry, setTelemetry] = useState<any>({
    current: {
      latency_ms: 24.0,
      packet_loss_pct: 0.8,
      bandwidth_mbps: 312.0,
      cpu_usage_pct: 68.0,
      device_id: 'SWI-03 (Building A)',
      device_status: 'Degraded'
    },
    history: [
      { time: '14:00', latency_ms: 20, packet_loss_pct: 0.4, bandwidth_mbps: 280, cpu_usage_pct: 55 },
      { time: '14:01', latency_ms: 22, packet_loss_pct: 0.5, bandwidth_mbps: 295, cpu_usage_pct: 58 },
      { time: '14:02', latency_ms: 28, packet_loss_pct: 0.9, bandwidth_mbps: 320, cpu_usage_pct: 65 },
      { time: '14:03', latency_ms: 25, packet_loss_pct: 0.7, bandwidth_mbps: 310, cpu_usage_pct: 64 },
      { time: '14:04', latency_ms: 24, packet_loss_pct: 0.8, bandwidth_mbps: 312, cpu_usage_pct: 68 },
    ]
  });

  const [loading, setLoading] = useState(false);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsData, telemData] = await Promise.all([
        api.getDashboardStats().catch(() => null),
        api.getDashboardTelemetry().catch(() => null)
      ]);
      if (statsData) setStats(statsData);
      if (telemData) setTelemetry(telemData);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AppLayout
      title="Network Command Centre"
      subtitle="Real-time network health, incidents and multi-agent operations."
    >
      {/* Top 4 Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric 1: Network Health */}
        <div className="glass-panel rounded-2xl p-4 flex items-center justify-between border-l-4 border-l-[#20E88A]">
          <div>
            <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">Network Health</p>
            <h2 className="text-3xl font-extrabold text-white mt-1">{stats.network_health_pct}%</h2>
            <p className="text-[10px] text-[#20E88A] flex items-center gap-1 mt-1 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-[#20E88A]" /> Baseline Optimal
            </p>
          </div>
          <div className="shrink-0">
            <ConfidenceGauge percentage={stats.network_health_pct} size={70} strokeWidth={6} />
          </div>
        </div>

        {/* Metric 2: AI Agents Online */}
        <div className="glass-panel rounded-2xl p-4 flex items-center justify-between border-l-4 border-l-[#A855F7]">
          <div>
            <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">AI Agents Online</p>
            <h2 className="text-3xl font-extrabold text-white mt-1">{stats.ai_agents_online}</h2>
            <p className="text-[10px] text-[#A855F7] mt-1 font-medium">Collaborating Engine</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#A855F7]/15 border border-[#A855F7]/30 flex items-center justify-center text-[#A855F7]">
            <Cpu className="w-6 h-6" />
          </div>
        </div>

        {/* Metric 3: Active Devices */}
        <div className="glass-panel rounded-2xl p-4 flex items-center justify-between border-l-4 border-l-[#438BFF]">
          <div>
            <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">Active Devices</p>
            <h2 className="text-3xl font-extrabold text-white mt-1">{stats.active_devices}</h2>
            <p className="text-[10px] text-[#438BFF] mt-1 font-medium">Campus Infrastructure</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#438BFF]/15 border border-[#438BFF]/30 flex items-center justify-center text-[#438BFF]">
            <Server className="w-6 h-6" />
          </div>
        </div>

        {/* Metric 4: Open Incidents */}
        <div className="glass-panel rounded-2xl p-4 flex items-center justify-between border-l-4 border-l-[#FF4568]">
          <div>
            <p className="text-[11px] font-semibold text-[#A9A3B8] uppercase tracking-wider">Open Incidents</p>
            <h2 className="text-3xl font-extrabold text-white mt-1">{stats.open_incidents}</h2>
            <Link to="/incidents/INC-1024" className="text-[10px] text-[#FF4568] hover:underline flex items-center gap-1 mt-1 font-medium">
              Review #INC-1024 <ArrowRight className="w-2.5 h-2.5" />
            </Link>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#FF4568]/15 border border-[#FF4568]/30 flex items-center justify-center text-[#FF4568]">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Main Interactive Topology and Live Telemetry Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: 3D Network Topology Center */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#FF781F] animate-pulse" />
              <h3 className="text-sm font-bold text-white tracking-wide">3D Network Topology Command View</h3>
            </div>
            <button
              onClick={fetchDashboardData}
              className="text-xs text-[#A9A3B8] hover:text-white flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#150f29] border border-[#2a1f42] transition-all"
            >
              <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin text-[#FF781F]' : ''}`} />
              <span>Refresh Telemetry</span>
            </button>
          </div>

          <Topology3D />
        </div>

        {/* Right 1 Col: Live Telemetry Sparkline Graphs */}
        <div className="space-y-3">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-sm font-bold text-white tracking-wide">Live Telemetry</h3>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#FF781F]/20 text-[#FF781F] border border-[#FF781F]/30 font-mono">
              SWI-03 (Building A)
            </span>
          </div>

          <div className="glass-panel rounded-2xl p-4 space-y-4">
            {/* Chart 1: Latency (ms) */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-[#A9A3B8] font-medium">Latency (ms)</span>
                <span className="font-mono font-bold text-[#A855F7]">{telemetry.current.latency_ms} ms</span>
              </div>
              <div className="h-12 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={telemetry.history}>
                    <Line type="monotone" dataKey="latency_ms" stroke="#A855F7" strokeWidth={2} dot={false} />
                    <Tooltip contentStyle={{ background: '#120c22', borderColor: '#A855F7', fontSize: 10 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 2: Packet Loss (%) */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-[#A9A3B8] font-medium">Packet Loss (%)</span>
                <span className="font-mono font-bold text-[#FF9B35]">{telemetry.current.packet_loss_pct}%</span>
              </div>
              <div className="h-12 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={telemetry.history}>
                    <Line type="monotone" dataKey="packet_loss_pct" stroke="#FF9B35" strokeWidth={2} dot={false} />
                    <Tooltip contentStyle={{ background: '#120c22', borderColor: '#FF9B35', fontSize: 10 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 3: Bandwidth (Mbps) */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-[#A9A3B8] font-medium">Bandwidth (Mbps)</span>
                <span className="font-mono font-bold text-[#20D9FF]">{telemetry.current.bandwidth_mbps} Mbps</span>
              </div>
              <div className="h-12 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={telemetry.history}>
                    <Line type="monotone" dataKey="bandwidth_mbps" stroke="#20D9FF" strokeWidth={2} dot={false} />
                    <Tooltip contentStyle={{ background: '#120c22', borderColor: '#20D9FF', fontSize: 10 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 4: CPU Usage (%) */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-[#A9A3B8] font-medium">CPU Usage</span>
                <span className="font-mono font-bold text-[#E040FB]">{telemetry.current.cpu_usage_pct}%</span>
              </div>
              <div className="h-12 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={telemetry.history}>
                    <Bar dataKey="cpu_usage_pct" fill="#E040FB" radius={[3, 3, 0, 0]} />
                    <Tooltip contentStyle={{ background: '#120c22', borderColor: '#E040FB', fontSize: 10 }} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
