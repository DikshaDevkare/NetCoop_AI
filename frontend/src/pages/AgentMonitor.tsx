import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { OrchestrationVisual } from '../components/agents/OrchestrationVisual';
import { api } from '../services/api';
import {
  Activity,
  Cpu,
  Clock,
  Terminal,
  FileCheck2,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Code2
} from 'lucide-react';

export const AgentMonitor: React.FC = () => {
  const [searchParams] = useSearchParams();
  const incidentId = searchParams.get('incident') || 'INC-1024';

  const [timeline, setTimeline] = useState<any[]>([
    { stage: 'init', title: 'Orchestrator initialized', time: '14:02:11', status: 'completed' },
    { stage: 'perf', title: 'Performance Agent analysis', time: '14:02:18', status: 'completed' },
    { stage: 'infra', title: 'Infrastructure analysis', time: '14:02:24', status: 'completed' },
    { stage: 'conn', title: 'Connectivity analysis', time: '14:02:29', status: 'completed' },
    { stage: 'corr', title: 'Fault correlation (running)', time: '14:02:35', status: 'running' },
    { stage: 'report', title: 'Generating recommendation', time: '...', status: 'pending' },
  ]);

  const [messages, setMessages] = useState<any[]>([
    {
      message_id: 'MSG-001',
      sender: 'performance_agent',
      receiver: 'fault_correlation_agent',
      display_tag: 'PerfAgent',
      summary: 'High CPU on SW-03 & latency spike (240ms)',
      timestamp: '14:02:18',
      payload: { finding: 'high_latency', metric: 'latency_ms', value: 240, unit: 'ms' }
    },
    {
      message_id: 'MSG-002',
      sender: 'infrastructure_agent',
      receiver: 'fault_correlation_agent',
      display_tag: 'InfraAgent',
      summary: 'Physical queue drops counter: 34 packets',
      timestamp: '14:02:24',
      payload: { finding: 'buffer_overflow', queue_drops: 34 }
    },
    {
      message_id: 'MSG-003',
      sender: 'connectivity_agent',
      receiver: 'fault_correlation_agent',
      display_tag: 'ConnAgent',
      summary: 'Increased queuing delay on uplink Gi0/1',
      timestamp: '14:02:29',
      payload: { finding: 'queuing_delay', status: 'degraded' }
    },
    {
      message_id: 'MSG-004',
      sender: 'fault_correlation_agent',
      receiver: 'reporting_agent',
      display_tag: 'CorrAgent',
      summary: 'Correlating evidence... Interface congestion (87%)',
      timestamp: '14:02:35',
      payload: { probable_cause: 'Interface congestion on SW-03', confidence: 0.87 }
    }
  ]);

  const [inspectedMessage, setInspectedMessage] = useState<any | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [msgsData, timeData] = await Promise.all([
          api.getAgentMessages(incidentId).catch(() => null),
          api.getExecutionTimeline(incidentId).catch(() => null)
        ]);
        if (msgsData && msgsData.length > 0) {
          setMessages(
            msgsData.map((m: any) => ({
              ...m,
              display_tag: m.sender ? m.sender.replace('_agent', '').substring(0, 7) : 'Agent',
              summary: m.payload?.finding || m.payload?.probable_cause || m.message_type
            }))
          );
        }
        if (timeData) setTimeline(timeData);
      } catch (e) {
        console.warn('Using baseline messages:', e);
      }
    };
    fetchData();
  }, [incidentId]);

  return (
    <AppLayout
      title="Multi-Agent Orchestration"
      subtitle="Five specialized agents collaborating for root-cause analysis."
    >
      {/* Top Action Bar */}
      <div className="flex items-center justify-between pb-2 border-b border-[#261d3b]">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-[#20E88A] animate-pulse" />
          <span className="text-xs text-[#A9A3B8]">Active Incident:</span>
          <span className="text-xs font-bold text-white font-mono">{incidentId}</span>
        </div>

        <Link
          to={`/diagnosis-report/${incidentId}`}
          className="px-4 py-1.5 rounded-xl bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-orange-500/20 hover:shadow-orange-500/40 transition-all"
        >
          <span>Open Full Diagnosis Report</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Main Grid: Left Orchestration Canvas, Right Timeline & Live Terminal Messages */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Central Orchestration Visual */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">Multi-Agent Collaboration Mesh</h3>
            <span className="text-[10px] text-[#A855F7] font-mono">NetCoop Agent Protocol v1.0</span>
          </div>

          <OrchestrationVisual />
        </div>

        {/* Right 1 Col: Execution Timeline & Live Structured Messages */}
        <div className="space-y-4">
          {/* Timeline Panel */}
          <div className="glass-panel rounded-2xl p-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
              <Clock className="w-3.5 h-3.5 text-[#FF781F]" />
              <span>Execution Timeline</span>
            </h3>
            <div className="space-y-2.5 text-xs">
              {timeline.map((step, idx) => (
                <div key={idx} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className={`w-2 h-2 rounded-full ${
                        step.status === 'completed'
                          ? 'bg-[#20E88A]'
                          : step.status === 'running'
                          ? 'bg-[#FF781F] animate-ping'
                          : 'bg-[#4a3b68]'
                      }`}
                    />
                    <span className="text-white text-[11px] font-medium">{step.title}</span>
                  </div>
                  <span className="text-[10px] font-mono text-[#A9A3B8]">{step.time}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Live Structured Messages Terminal */}
          <div className="glass-panel rounded-2xl p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5 text-[#20D9FF]" />
                <span>Live Messages</span>
              </h3>
              <span className="text-[9px] text-[#A9A3B8]">Click to inspect JSON</span>
            </div>

            <div className="space-y-2 bg-[#0c0817] p-2.5 rounded-xl border border-[#211636] font-mono text-[11px] max-h-48 overflow-y-auto">
              {messages.map((m, idx) => (
                <div
                  key={idx}
                  onClick={() => setInspectedMessage(m)}
                  className="p-1.5 rounded hover:bg-[#1a122e] cursor-pointer transition-all flex items-start justify-between group"
                >
                  <div className="truncate">
                    <span className="text-[#FF781F] font-semibold">[{m.display_tag || m.sender}]</span>{' '}
                    <span className="text-[#e2dcfa] text-[10px] group-hover:text-white">{m.summary}</span>
                  </div>
                  <span className="text-[9px] text-[#7d7494] shrink-0 ml-2">{m.timestamp || '14:02'}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Structured JSON Message Inspection Modal */}
      {inspectedMessage && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-[#120b22] border border-[#FF781F]/40 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-[#2a1d42] pb-3">
              <div className="flex items-center gap-2">
                <Code2 className="w-5 h-5 text-[#FF781F]" />
                <h4 className="text-sm font-bold text-white">NetCoop Agent Message Inspection</h4>
              </div>
              <button
                onClick={() => setInspectedMessage(null)}
                className="text-xs text-[#A9A3B8] hover:text-white px-2 py-1 rounded bg-[#201538]"
              >
                ✕
              </button>
            </div>
            <div className="text-xs text-[#A9A3B8] flex justify-between">
              <span>Sender: <strong className="text-white">{inspectedMessage.sender}</strong></span>
              <span>Receiver: <strong className="text-white">{inspectedMessage.receiver}</strong></span>
            </div>
            <pre className="p-3 rounded-xl bg-[#080510] border border-[#261a3d] text-[11px] font-mono text-[#20D9FF] overflow-x-auto max-h-64">
              {JSON.stringify(inspectedMessage, null, 2)}
            </pre>
            <button
              onClick={() => setInspectedMessage(null)}
              className="w-full py-2 bg-[#FF781F] text-white text-xs font-bold rounded-xl"
            >
              Close Inspector
            </button>
          </div>
        </div>
      )}
    </AppLayout>
  );
};
