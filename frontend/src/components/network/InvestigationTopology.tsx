import React, { useState } from 'react';
import { Building2, Server, Network, AlertCircle, CheckCircle2, AlertTriangle } from 'lucide-react';

interface NetworkNode {
  id: string;
  name: string;
  sublabel: string;
  status: 'Critical' | 'Healthy' | 'Degraded';
  color: string;
  x: number;
  y: number;
}

export const InvestigationTopology: React.FC<{ onNodeSelect?: (nodeId: string) => void }> = ({ onNodeSelect }) => {
  const [activeNode, setActiveNode] = useState('bldg_a');

  const nodes: NetworkNode[] = [
    { id: 'bldg_a', name: 'Building A', sublabel: '(Affected)', status: 'Critical', color: '#FF4568', x: 22, y: 62 },
    { id: 'core_b', name: 'Core B', sublabel: '(Healthy)', status: 'Healthy', color: '#20D9FF', x: 50, y: 44 },
    { id: 'bldg_b', name: 'Building B', sublabel: '(Healthy)', status: 'Healthy', color: '#20E88A', x: 78, y: 30 },
    { id: 'branch_c', name: 'Branch C', sublabel: '(Degraded)', status: 'Degraded', color: '#FFC247', x: 74, y: 72 }
  ];

  const handleSelect = (id: string) => {
    setActiveNode(id);
    if (onNodeSelect) onNodeSelect(id);
  };

  return (
    <div className="relative w-full h-[320px] rounded-2xl bg-gradient-to-b from-[#130d24] via-[#0d091a] to-[#070510] border border-[#261d3b] p-4 overflow-hidden flex items-center justify-center">
      {/* Dynamic Laser Connection Pathways */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <line x1="22%" y1="62%" x2="50%" y2="44%" stroke="#FF4568" strokeWidth="2.5" strokeDasharray="5 5" className="animate-energy-flow" />
        <line x1="50%" y1="44%" x2="78%" y2="30%" stroke="#20D9FF" strokeWidth="2" strokeDasharray="5 5" className="animate-energy-flow" />
        <line x1="50%" y1="44%" x2="74%" y2="72%" stroke="#FFC247" strokeWidth="2" strokeDasharray="5 5" className="animate-energy-flow" />
      </svg>

      {/* Nodes */}
      {nodes.map((node) => {
        const isSelected = activeNode === node.id;
        return (
          <div
            key={node.id}
            onClick={() => handleSelect(node.id)}
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
            className={`absolute -translate-x-1/2 -translate-y-1/2 cursor-pointer group transition-all duration-300 z-10 ${
              isSelected ? 'scale-115' : 'hover:scale-105'
            }`}
          >
            {/* Glow Aura */}
            <div
              className="absolute -inset-4 rounded-full blur-md opacity-50 group-hover:opacity-90 transition-opacity pointer-events-none"
              style={{ backgroundColor: node.color }}
            />

            {/* 3D Isometric Card */}
            <div
              className="relative px-3.5 py-2.5 rounded-xl border backdrop-blur-md flex flex-col items-center justify-center shadow-xl transition-all"
              style={{
                backgroundColor: isSelected ? `${node.color}25` : '#160f29/90',
                borderColor: node.color,
                boxShadow: isSelected ? `0 0 20px ${node.color}50` : 'none'
              }}
            >
              <Building2 className="w-5 h-5 mb-1" style={{ color: node.color }} />
              <span className="text-[10px] font-bold text-white tracking-wide">{node.name}</span>
              <span className="text-[9px] font-semibold" style={{ color: node.color }}>
                {node.sublabel}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
};
