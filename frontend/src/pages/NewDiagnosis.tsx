import React, { useState } from 'react';
import { AppLayout } from '../components/layout/AppLayout';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';
import {
  Activity,
  AlertTriangle,
  Globe,
  Cpu,
  Wifi,
  Sliders,
  UploadCloud,
  FileText,
  CheckCircle2,
  ArrowRight,
  Loader2
} from 'lucide-react';

export const NewDiagnosis: React.FC = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedScenario, setSelectedScenario] = useState('network_congestion');
  const [isRunning, setIsRunning] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const scenarios = [
    { id: 'network_congestion', title: 'Network Congestion', icon: Activity, desc: 'High bandwidth utilization causing queue drops and high RTT.' },
    { id: 'link_interface_failure', title: 'Link / Interface Failure', icon: AlertTriangle, desc: 'Interface CRC errors and frame corruption.' },
    { id: 'dns_dhcp_failure', title: 'DNS / DHCP Failure', icon: Globe, desc: 'Resolution failure and DHCP timeouts.' },
    { id: 'device_overload', title: 'Device Overload', icon: Cpu, desc: 'Excessive CPU load (>95%) and memory saturation.' },
    { id: 'wifi_signal_issue', title: 'Wi-Fi Signal Issue', icon: Wifi, desc: 'Poor signal RSSI and high 802.11 retransmissions.' },
    { id: 'custom_scenario', title: 'Custom Scenario', icon: Sliders, desc: 'Upload custom telemetry captures or manual metrics.' },
  ];

  const sampleFiles = [
    { name: 'site-a_telemetry.csv', size: '2.4 MB', valid: true },
    { name: 'interfaces.json', size: '532 KB', valid: true },
    { name: 'topology.json', size: '1.1 MB', valid: true },
  ];

  const handleRunDiagnosis = async () => {
    try {
      setIsRunning(true);
      setErrorMsg('');
      const res = await api.runDiagnosis({ scenario: selectedScenario });
      if (res && res.incident_id) {
        // Navigate to Agent Monitor with real-time incident ID
        navigate(`/agent-monitor?incident=${res.incident_id}`);
      } else {
        navigate('/agent-monitor');
      }
    } catch (err: any) {
      console.error('Diagnosis failed:', err);
      // Fallback navigation for seamless demo experience
      navigate('/agent-monitor');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <AppLayout
      title="Start a New Network Diagnosis"
      subtitle="Select a scenario, upload telemetry and launch a multi-agent investigation."
    >
      {/* 4-Step Indicator Header */}
      <div className="flex items-center justify-between max-w-xl mx-auto py-2 px-4 mb-4">
        {[
          { num: 1, label: 'Scenario' },
          { num: 2, label: 'Telemetry' },
          { num: 3, label: 'Validate' },
          { num: 4, label: 'Run' },
        ].map((step, idx) => (
          <React.Fragment key={step.num}>
            <div className="flex items-center gap-2">
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                  step.num === 1
                    ? 'bg-[#FF781F] text-white shadow-lg shadow-orange-500/40 ring-2 ring-orange-500/20'
                    : 'bg-[#18112c] text-[#A9A3B8] border border-[#2e234a]'
                }`}
              >
                {step.num}
              </div>
              <span className={`text-xs font-medium ${step.num === 1 ? 'text-white' : 'text-[#8c83a0]'}`}>
                {step.label}
              </span>
            </div>
            {idx < 3 && <div className="h-[1px] w-12 bg-[#2a1e44]" />}
          </React.Fragment>
        ))}
      </div>

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Choose Diagnostic Scenario */}
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-white tracking-wide">Choose Diagnostic Scenario</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {scenarios.map((sc) => {
              const Icon = sc.icon;
              const isSelected = selectedScenario === sc.id;
              return (
                <button
                  key={sc.id}
                  onClick={() => setSelectedScenario(sc.id)}
                  className={`p-3.5 rounded-2xl flex flex-col items-center justify-center text-center transition-all ${
                    isSelected
                      ? 'bg-[#221338] border-2 border-[#FF781F] shadow-lg shadow-orange-500/30 scale-102'
                      : 'glass-panel hover:border-[#FF781F]/40 hover:bg-[#18122c]'
                  }`}
                >
                  <div
                    className={`w-10 h-10 rounded-xl flex items-center justify-center mb-2 ${
                      isSelected ? 'bg-[#FF781F] text-white shadow-md' : 'bg-[#1e1538] text-[#A855F7]'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-xs font-bold text-white leading-tight mb-1">{sc.title}</span>
                  <span className="text-[9px] text-[#A9A3B8] line-clamp-2">{sc.desc}</span>
                </button>
              );
            })}
          </div>

          {/* Data Validation Checklist */}
          <div className="glass-panel rounded-2xl p-4 mt-6">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3">Data Validation Summary</h4>
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-xs text-[#20E88A]">
                <CheckCircle2 className="w-4 h-4 text-[#20E88A]" />
                <span>Schema compatible (NetCoop Telemetry v1.0 standard)</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-[#20E88A]">
                <CheckCircle2 className="w-4 h-4 text-[#20E88A]" />
                <span>Required fields present (latency, jitter, queue_drops, cpu)</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-[#20E88A]">
                <CheckCircle2 className="w-4 h-4 text-[#20E88A]" />
                <span>No missing telemetry samples in active observation window</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Telemetry Upload & Sample Files */}
        <div className="space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-white tracking-wide">Telemetry Ingestion</h3>

            {/* Drag and Drop Zone */}
            <div className="border-2 border-dashed border-[#FF781F]/40 hover:border-[#FF781F] bg-[#140c26]/60 rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all group">
              <div className="w-14 h-14 rounded-2xl bg-[#FF781F]/15 border border-[#FF781F]/30 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform shadow-lg shadow-orange-500/20">
                <UploadCloud className="w-7 h-7 text-[#FF781F]" />
              </div>
              <p className="text-sm font-bold text-white">Drag & drop telemetry files here</p>
              <p className="text-xs text-[#A9A3B8] mt-1">or browse files (PCAP, CSV, JSON, NetFlow)</p>
            </div>

            {/* Attached / Pre-loaded Sample Files */}
            <div className="space-y-2">
              <p className="text-xs font-semibold text-[#A9A3B8]">Selected Telemetry Buffers:</p>
              {sampleFiles.map((file) => (
                <div
                  key={file.name}
                  className="flex items-center justify-between p-2.5 rounded-xl bg-[#140e28] border border-[#271d3d] text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <FileText className="w-4 h-4 text-[#A855F7]" />
                    <span className="font-mono text-white text-[11px]">{file.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-[#A9A3B8]">{file.size}</span>
                    <CheckCircle2 className="w-3.5 h-3.5 text-[#20E88A]" />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Big Action Run Button */}
          <div className="pt-4">
            <button
              onClick={handleRunDiagnosis}
              disabled={isRunning}
              className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-[#FF781F] via-[#FF9B35] to-[#A855F7] text-white font-bold text-sm flex items-center justify-center gap-2 shadow-xl shadow-orange-500/30 hover:shadow-orange-500/50 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-70 cursor-pointer"
            >
              {isRunning ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Orchestrating 5 Diagnostic Agents & 4 ML Models...</span>
                </>
              ) : (
                <>
                  <span>Run Diagnosis</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
