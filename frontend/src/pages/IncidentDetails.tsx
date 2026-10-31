import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { InvestigationTopology } from '../components/network/InvestigationTopology';
import { api } from '../services/api';
import {
  AlertTriangle,
  Server,
  Layers,
  ArrowRight,
  Clock,
  CheckCircle2,
  Cpu,
  BarChart2,
  FileText
} from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, Tooltip } from 'recharts';

export const IncidentDetails: React.FC = () => {
  const { id = 'INC-1024' } = useParams();
  const [activeTab, setActiveTab] = useState<'Overview' | 'Telemetry' | 'Topology' | 'Affected Devices' | 'Logs'>('Topology');
  const [incident, setIncident] = useState<any>({
    incident_id: id,
    title: 'Network congestion on Building A',
    subtitle: 'Network congestion on Building A • Detected 5 mins ago',
    severity: 'High',
    status: 'In Progress',
    device_details: {
      device_id: 'SWI-03 (Building A)',
      status: 'Degraded',
      cpu_usage: 78,
      memory_usage: 64,
      interface_errors: 126,
      queue_drops: 34,
      link_utilization: 92
    },
    telemetry_trend: [
      { time: '13:50', link_util: 55, latency: 22 },
      { time: '13:55', link_util: 68, latency: 28 },
      { time: '14:00', link_util: 84, latency: 85 },
      { time: '14:02', link_util: 92, latency: 195 },
      { time: '14:05', link_util: 94, latency: 240 }
    ]
  });

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const data = await api.getIncidentDetails(id);
        if (data) setIncident(data);
      } catch (err) {
        console.warn('Using baseline incident details:', err);
      }
    };
    fetchIncident();
  }, [id]);

  const tabs: Array<'Overview' | 'Telemetry' | 'Topology' | 'Affected Devices' | 'Logs'> = [
    'Overview',
    'Telemetry',
    'Topology',
    'Affected Devices',
    'Logs'
  ];

  return (
    <AppLayout
      title={`Incident #${incident.incident_id}`}
      subtitle={incident.subtitle}
    >
      {/* Top Banner with Severity & Status Badges */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-[#261d3b]">
        <div className="flex items-center gap-3">
          <span className="text-sm font-bold text-white font-mono">Incident #{incident.incident_id}</span>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-[#FF4568]/20 text-[#FF4568] border border-[#FF4568]/40">
            {incident.severity}
          </span>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#FF781F]/20 text-[#FF781F] border border-[#FF781F]/40">
            {incident.status}
          </span>
        </div>

        <Link
          to={`/diagnosis-report/${incident.incident_id}`}
          className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-orange-500/20 hover:shadow-orange-500/40 transition-all"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>View Diagnosis Report</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-[#261d3b]">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 text-xs font-bold transition-all relative ${
              activeTab === tab
                ? 'text-[#FF781F] border-b-2 border-[#FF781F]'
                : 'text-[#A9A3B8] hover:text-white'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Main Grid: Left Topology Visualization, Right Device Details HUD */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Network Topology Inspection Visual */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">Affected Infrastructure Topology</h3>
            <span className="text-[10px] text-[#A9A3B8]">Building A → Core B → Building B / Branch C</span>
          </div>

          <InvestigationTopology />
        </div>

        {/* Right 1 Col: Device Details Panel */}
        <div className="space-y-3">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">Device Details</h3>
            <span className="px-2 py-0.5 rounded bg-[#FF781F]/20 text-[#FF781F] text-[10px] font-bold uppercase">
              {incident.device_details.status}
            </span>
          </div>

          <div className="glass-panel rounded-2xl p-4 space-y-4">
            <div>
              <p className="text-sm font-bold text-white">{incident.device_details.device_id}</p>
              <p className="text-[10px] text-[#A9A3B8]">Cisco Catalyst Campus Distribution Switch</p>
            </div>

            {/* Progress Bar 1: CPU Usage */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#A9A3B8]">CPU Usage</span>
                <span className="font-mono font-bold text-[#FF9B35]">{incident.device_details.cpu_usage}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-[#201538] overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[#FF781F] to-[#FF4568] rounded-full"
                  style={{ width: `${incident.device_details.cpu_usage}%` }}
                />
              </div>
            </div>

            {/* Progress Bar 2: Memory */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#A9A3B8]">Memory</span>
                <span className="font-mono font-bold text-[#FFC247]">{incident.device_details.memory_usage}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-[#201538] overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[#FFC247] to-[#FF9B35] rounded-full"
                  style={{ width: `${incident.device_details.memory_usage}%` }}
                />
              </div>
            </div>

            {/* Counters */}
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-2.5 rounded-xl bg-[#140e26] border border-[#2b1f44]">
                <p className="text-[10px] text-[#A9A3B8]">Interface Errors</p>
                <p className="text-lg font-bold font-mono text-[#FF4568]">{incident.device_details.interface_errors}</p>
              </div>
              <div className="p-2.5 rounded-xl bg-[#140e26] border border-[#2b1f44]">
                <p className="text-[10px] text-[#A9A3B8]">Queue Drops</p>
                <p className="text-lg font-bold font-mono text-[#FF9B35]">{incident.device_details.queue_drops}</p>
              </div>
            </div>

            {/* Link Utilization Chart */}
            <div className="pt-2">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#A9A3B8]">Link Utilization</span>
                <span className="font-mono font-bold text-[#FF781F]">{incident.device_details.link_utilization}%</span>
              </div>
              <div className="h-16 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={incident.telemetry_trend}>
                    <Line type="monotone" dataKey="link_util" stroke="#FF781F" strokeWidth={2} dot={false} />
                    <Tooltip contentStyle={{ background: '#120c22', borderColor: '#FF781F', fontSize: 10 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
