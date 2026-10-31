import React, { useState } from 'react';
import { Router, Server, Wifi, Cpu, ShieldAlert, CheckCircle2, AlertTriangle } from 'lucide-react';

interface DeviceNode {
  id: string;
  name: string;
  type: string;
  status: 'Healthy' | 'Degraded' | 'Critical' | 'Online';
  cpu: number;
  memory: number;
  latency: number;
  loss: number;
  x: number; // percentage
  y: number; // percentage
  icon: any;
}

export const Topology3D: React.FC<{ onSelectDevice?: (dev: DeviceNode) => void }> = ({ onSelectDevice }) => {
  const [selected, setSelected] = useState<DeviceNode | null>(null);

  const nodes: DeviceNode[] = [
    {
      id: 'branch_rtr_01',
      name: 'Branch Router',
      type: 'Core Gateway',
      status: 'Degraded',
      cpu: 78,
      memory: 64,
      latency: 24.0,
      loss: 0.8,
      x: 50,
      y: 50,
      icon: Router
    },
    {
      id: 'core_sw_01',
      name: 'Core Switch',
      type: 'Layer 3 Switch',
      status: 'Healthy',
      cpu: 32,
      memory: 45,
      latency: 4.2,
      loss: 0.0,
      x: 24,
      y: 35,
      icon: Server
    },
    {
      id: 'access_point_01',
      name: 'Access Point',
      type: 'Wi-Fi 6 AP',
      status: 'Online',
      cpu: 28,
      memory: 38,
      latency: 12.5,
      loss: 0.1,
      x: 76,
      y: 32,
      icon: Wifi
    },
    {
      id: 'swi_03_bldg_a',
      name: 'SWI-03 (Building A)',
      type: 'Distribution Switch',
      status: 'Degraded',
      cpu: 82,
      memory: 68,
      latency: 28.5,
      loss: 1.4,
      x: 28,
      y: 72,
      icon: Server
    },
    {
      id: 'server_dns_01',
      name: 'DNS / DHCP Core',
      type: 'Core Server',
      status: 'Healthy',
      cpu: 34,
      memory: 42,
      latency: 5.8,
      loss: 0.0,
      x: 74,
      y: 70,
      icon: Cpu
    }
  ];

  const handleNodeClick = (node: DeviceNode) => {
    setSelected(node);
    if (onSelectDevice) onSelectDevice(node);
  };

  return (
    <div className="relative w-full h-[380px] rounded-2xl bg-gradient-to-b from-[#130d24] via-[#0d091a] to-[#070510] border border-[#261d3b] p-4 overflow-hidden shadow-2xl flex items-center justify-center">
      {/* 3D Grid Platform with Isometric Perspective */}
      <div
        className="absolute inset-0 pointer-events-none opacity-40"
        style={{
          background: 'radial-gradient(ellipse at 50% 55%, rgba(255, 120, 31, 0.18) 0%, rgba(168, 85, 247, 0.08) 40%, transparent 75%)',
        }}
      />

      {/* SVG Connecting Conduits with Laser Energy Particles */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <defs>
          <linearGradient id="laserOrange" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FF781F" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#A855F7" stopOpacity="0.8" />
          </linearGradient>
          <linearGradient id="laserCyan" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#20D9FF" stopOpacity="0.7" />
            <stop offset="100%" stopColor="#FF781F" stopOpacity="0.7" />
          </linearGradient>
        </defs>

        {/* Laser Conduits connecting outer nodes to central Branch Router */}
        <line x1="50%" y1="50%" x2="24%" y2="35%" stroke="url(#laserOrange)" strokeWidth="2.5" strokeDasharray="6 6" className="animate-energy-flow" />
        <line x1="50%" y1="50%" x2="76%" y2="32%" stroke="url(#laserCyan)" strokeWidth="2.5" strokeDasharray="6 6" className="animate-energy-flow" />
        <line x1="50%" y1="50%" x2="28%" y2="72%" stroke="#FF4568" strokeWidth="2" strokeDasharray="5 5" className="animate-energy-flow" />
        <line x1="50%" y1="50%" x2="74%" y2="70%" stroke="#20D9FF" strokeWidth="2" strokeDasharray="5 5" className="animate-energy-flow" />
      </svg>

      {/* Render 3D Platform Pedestals and Nodes */}
      {nodes.map((node) => {
        const Icon = node.icon;
        const isCenter = node.id === 'branch_rtr_01';
        const isSelected = selected?.id === node.id;

        const statusColor =
          node.status === 'Healthy' || node.status === 'Online'
            ? '#20E88A'
            : node.status === 'Degraded'
            ? '#FF781F'
            : '#FF4568';

        return (
          <div
            key={node.id}
            onClick={() => handleNodeClick(node)}
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
            className={`absolute -translate-x-1/2 -translate-y-1/2 cursor-pointer group transition-all duration-300 z-10 ${
              isSelected ? 'scale-115' : 'hover:scale-110'
            }`}
          >
            {/* 3D Isometric Base Glow */}
            <div
              className="absolute -inset-4 rounded-full blur-md opacity-40 group-hover:opacity-80 transition-opacity pointer-events-none"
              style={{ backgroundColor: statusColor }}
            />

            {/* Futuristic 3D Pod */}
            <div
              className={`relative flex flex-col items-center justify-center rounded-2xl p-3 border transition-all ${
                isCenter
                  ? 'w-24 h-24 bg-gradient-to-b from-[#2a1738] to-[#120a22] border-[#FF781F] shadow-lg shadow-orange-500/40 ring-2 ring-orange-500/20'
                  : 'w-18 h-18 bg-[#18112c]/90 border-[#32244d] hover:border-[#FF781F]/70 shadow-xl'
              }`}
            >
              <div
                className="w-9 h-9 rounded-xl flex items-center justify-center mb-1.5 shadow-inner"
                style={{ backgroundColor: `${statusColor}22` }}
              >
                <Icon className="w-5 h-5" style={{ color: statusColor }} />
              </div>

              {/* Status Indicator Badge */}
              <div className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: statusColor }} />
                <span className="text-[9px] font-bold text-white tracking-wider truncate max-w-[65px]">
                  {node.name}
                </span>
              </div>

              {/* Status Label Pill */}
              <span
                className="text-[8px] font-semibold uppercase tracking-wider mt-0.5 px-1 rounded"
                style={{ color: statusColor, backgroundColor: `${statusColor}18` }}
              >
                {node.status}
              </span>
            </div>

            {/* Hover Tooltip Card */}
            <div className="absolute left-1/2 -translate-x-1/2 -bottom-16 w-36 bg-[#160f2a]/95 border border-[#3b2b5a] rounded-xl p-2 text-left opacity-0 group-hover:opacity-100 pointer-events-none transition-all shadow-2xl z-30">
              <p className="text-[10px] font-bold text-white">{node.name}</p>
              <div className="text-[9px] text-[#A9A3B8] flex justify-between mt-0.5">
                <span>CPU: {node.cpu}%</span>
                <span>Lat: {node.latency}ms</span>
              </div>
              <div className="text-[9px] text-[#A9A3B8] flex justify-between">
                <span>Mem: {node.memory}%</span>
                <span>Loss: {node.loss}%</span>
              </div>
            </div>
          </div>
        );
      })}

      {/* Selected Node Details Floating HUD */}
      {selected && (
        <div className="absolute bottom-3 left-3 bg-[#130d24]/90 backdrop-blur-md border border-[#FF781F]/40 rounded-xl px-4 py-2.5 flex items-center gap-4 text-xs z-20 shadow-2xl">
          <div>
            <p className="text-[10px] text-[#A9A3B8] uppercase tracking-wider">Inspecting Node</p>
            <p className="font-bold text-white">{selected.name}</p>
          </div>
          <div className="h-6 w-[1px] bg-[#32244d]" />
          <div>
            <p className="text-[10px] text-[#A9A3B8]">CPU / Mem</p>
            <p className="font-mono text-[#FF9B35] font-semibold">{selected.cpu}% / {selected.memory}%</p>
          </div>
          <div className="h-6 w-[1px] bg-[#32244d]" />
          <div>
            <p className="text-[10px] text-[#A9A3B8]">Latency / Loss</p>
            <p className="font-mono text-[#20D9FF] font-semibold">{selected.latency}ms / {selected.loss}%</p>
          </div>
          <button
            onClick={() => setSelected(null)}
            className="text-[10px] text-[#A9A3B8] hover:text-white ml-2"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
};
