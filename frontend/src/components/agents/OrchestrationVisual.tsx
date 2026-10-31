import React, { useState } from 'react';
import { Zap, Cpu, Radio, GitBranch, FileCheck2, Activity, Play } from 'lucide-react';

interface AgentInfo {
  id: string;
  name: string;
  status: string;
  color: string;
  x: number; // percentage
  y: number; // percentage
  icon: any;
  findingSummary: string;
}

export const OrchestrationVisual: React.FC<{ onAgentSelect?: (agentId: string) => void }> = ({ onAgentSelect }) => {
  const [selectedAgent, setSelectedAgent] = useState<string>('fault_correlation_agent');

  const agents: AgentInfo[] = [
    {
      id: 'performance_agent',
      name: 'Performance Agent',
      status: 'Active',
      color: '#A855F7',
      x: 50,
      y: 18,
      icon: Zap,
      findingSummary: 'High latency (240ms) & link queue drops on SW-03'
    },
    {
      id: 'infrastructure_agent',
      name: 'Infrastructure Health Agent',
      status: 'Done',
      color: '#20E88A',
      x: 18,
      y: 44,
      icon: Cpu,
      findingSummary: 'Elevated CPU (78%) and memory pressure (64%)'
    },
    {
      id: 'connectivity_agent',
      name: 'Connectivity Analysis Agent',
      status: 'Processing...',
      color: '#20D9FF',
      x: 82,
      y: 44,
      icon: Radio,
      findingSummary: 'DNS latency verified normal; Wi-Fi metrics non-applicable'
    },
    {
      id: 'fault_correlation_agent',
      name: 'Fault Correlation Agent',
      status: 'Running...',
      color: '#E040FB',
      x: 28,
      y: 80,
      icon: GitBranch,
      findingSummary: 'Fusing evidence: Interface congestion confirmed (87% conf)'
    },
    {
      id: 'reporting_agent',
      name: 'Recommendation & Reporting Agent',
      status: 'Standby',
      color: '#FF9B35',
      x: 72,
      y: 80,
      icon: FileCheck2,
      findingSummary: 'Action playbook: Rate-limiting & QoS prioritization queued'
    }
  ];

  const handleSelect = (id: string) => {
    setSelectedAgent(id);
    if (onAgentSelect) onAgentSelect(id);
  };

  return (
    <div className="relative w-full h-[430px] rounded-2xl bg-gradient-to-b from-[#120b22] via-[#0d081a] to-[#070510] border border-[#2a1d42] p-4 overflow-hidden flex items-center justify-center shadow-2xl">
      {/* Central Concentric Glow Waves */}
      <div className="absolute w-72 h-72 rounded-full border border-[#FF781F]/20 animate-ping opacity-20 pointer-events-none" />
      <div className="absolute w-52 h-52 rounded-full border border-[#A855F7]/30 pointer-events-none" />
      <div className="absolute w-36 h-36 rounded-full border border-[#FF781F]/40 animate-pulse pointer-events-none" />

      {/* SVG Connecting Conduits from Orchestrator to all 5 agents */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        {agents.map((ag) => (
          <line
            key={ag.id}
            x1="50%"
            y1="50%"
            x2={`${ag.x}%`}
            y2={`${ag.y}%`}
            stroke={ag.color}
            strokeWidth="2"
            strokeDasharray="6 6"
            className="animate-energy-flow"
          />
        ))}
      </svg>

      {/* Center Orchestrator Node */}
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center">
        <div className="relative w-24 h-24 rounded-full bg-gradient-to-tr from-[#FF781F] via-[#FF9B35] to-[#A855F7] p-1 shadow-2xl shadow-orange-500/50 flex items-center justify-center animate-pulse">
          <div className="w-full h-full bg-[#140b25] rounded-full flex flex-col items-center justify-center p-2 text-center">
            <Activity className="w-6 h-6 text-[#FF781F] mb-0.5" />
            <span className="text-[10px] font-extrabold text-white tracking-widest uppercase">Orchestrator</span>
            <span className="text-[8px] text-[#20E88A] font-semibold">Active</span>
          </div>
        </div>
      </div>

      {/* Outer 5 Agents */}
      {agents.map((ag) => {
        const Icon = ag.icon;
        const isSelected = selectedAgent === ag.id;

        return (
          <div
            key={ag.id}
            onClick={() => handleSelect(ag.id)}
            style={{ left: `${ag.x}%`, top: `${ag.y}%` }}
            className={`absolute -translate-x-1/2 -translate-y-1/2 cursor-pointer group transition-all duration-300 z-10 ${
              isSelected ? 'scale-115' : 'hover:scale-110'
            }`}
          >
            {/* Glow Halo */}
            <div
              className="absolute -inset-3 rounded-full blur-md opacity-40 group-hover:opacity-80 transition-opacity pointer-events-none"
              style={{ backgroundColor: ag.color }}
            />

            {/* Circular Agent Pod */}
            <div
              className="relative w-18 h-18 rounded-2xl p-2.5 flex flex-col items-center justify-center border shadow-xl backdrop-blur-md transition-all text-center"
              style={{
                backgroundColor: isSelected ? `${ag.color}28` : '#160f2a/95',
                borderColor: ag.color,
                boxShadow: isSelected ? `0 0 25px ${ag.color}60` : 'none'
              }}
            >
              <div
                className="w-8 h-8 rounded-xl flex items-center justify-center mb-1 shadow-inner"
                style={{ backgroundColor: `${ag.color}22` }}
              >
                <Icon className="w-4 h-4" style={{ color: ag.color }} />
              </div>
              <span className="text-[8px] font-bold text-white tracking-wider max-w-[65px] truncate">
                {ag.name.replace(' Agent', '')}
              </span>
              <span
                className="text-[7px] font-semibold mt-0.5 px-1 rounded uppercase tracking-wider"
                style={{ color: ag.color, backgroundColor: `${ag.color}20` }}
              >
                {ag.status}
              </span>
            </div>
          </div>
        );
      })}

      {/* Selected Agent HUD Tooltip */}
      {selectedAgent && (
        <div className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-[#140b25]/95 border border-[#3b2b5a] rounded-xl px-4 py-2 flex items-center gap-3 text-xs shadow-2xl z-30">
          <span className="w-2 h-2 rounded-full bg-[#FF781F] animate-ping" />
          <div>
            <span className="text-[10px] text-[#A9A3B8] uppercase tracking-wider">Inspecting Agent: </span>
            <span className="font-bold text-white">
              {agents.find((a) => a.id === selectedAgent)?.name}
            </span>
            <p className="text-[10px] text-[#FF9B35]">
              {agents.find((a) => a.id === selectedAgent)?.findingSummary}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
