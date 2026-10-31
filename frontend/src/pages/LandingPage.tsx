import React from 'react';
import { Link } from 'react-router-dom';
import { LivingBackground } from '../components/layout/LivingBackground';
import {
  Zap,
  Cpu,
  Layers,
  ArrowRight,
  ShieldCheck,
  Activity,
  Server,
  Globe,
  Radio,
  GitBranch,
  FileCheck2,
  Lock,
  Sparkles,
  AlertTriangle
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="relative min-h-screen bg-[#070711] text-[#F5F2FA] overflow-x-hidden">
      <LivingBackground />

      {/* Navigation Bar */}
      <header className="relative z-20 max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#FF781F] via-[#FF9B35] to-[#A855F7] p-0.5 flex items-center justify-center shadow-lg shadow-orange-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-[#120c22] rounded-[10px] flex items-center justify-center">
              <Zap className="w-5 h-5 text-[#FF781F]" />
            </div>
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-wider text-white">NetCoop</span>
            <span className="font-bold text-xs px-1.5 py-0.5 rounded bg-[#FF781F]/20 text-[#FF781F] border border-[#FF781F]/40 ml-1.5">AI</span>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-8 text-xs font-semibold text-[#A9A3B8]">
          <a href="#agents" className="hover:text-white transition-colors">Agents</a>
          <a href="#models" className="hover:text-white transition-colors">ML Modules</a>
          <a href="#interop" className="hover:text-white transition-colors">Protocol</a>
          <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
        </nav>

        <div className="flex items-center gap-3">
          <Link
            to="/login"
            className="px-4 py-2 rounded-xl text-xs font-bold text-[#A9A3B8] hover:text-white hover:bg-[#1a122e] transition-all"
          >
            Sign In
          </Link>
          <Link
            to="/dashboard"
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white font-bold text-xs shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:scale-105 transition-all"
          >
            Launch Command Centre
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pt-12 pb-24 text-center flex flex-col items-center">
        {/* Subtitle Pill */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#FF781F]/15 border border-[#FF781F]/30 text-[#FF781F] text-xs font-extrabold tracking-widest uppercase mb-6 shadow-lg shadow-orange-500/10">
          <Sparkles className="w-3.5 h-3.5" />
          <span>MULTI-AGENT NETWORK INTELLIGENCE</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl leading-[1.1] mb-6">
          Transform Network Complexity Into{' '}
          <span className="bg-gradient-to-r from-[#FF781F] via-[#FF9B35] to-[#A855F7] bg-clip-text text-transparent">
            Intelligent Clarity.
          </span>
        </h1>

        {/* Supporting text */}
        <p className="text-base sm:text-lg text-[#A9A3B8] max-w-2xl leading-relaxed mb-10">
          An interoperable multi-agent intelligence platform that investigates network faults,
          correlates telemetry and delivers explainable root-cause insights across campus infrastructure.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
          <Link
            to="/dashboard"
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-[#FF781F] via-[#FF9B35] to-[#A855F7] text-white font-bold text-sm shadow-xl shadow-orange-500/30 hover:shadow-orange-500/60 hover:scale-105 transition-all flex items-center gap-2"
          >
            <span>Launch Network Command Centre</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <a
            href="#agents"
            className="px-8 py-4 rounded-xl glass-panel text-white font-bold text-sm hover:border-[#FF781F]/50 hover:bg-[#1a122e] transition-all"
          >
            Explore Architecture
          </a>
        </div>

        {/* Hero 3D Network Visualization Preview */}
        <div className="w-full max-w-5xl rounded-3xl p-1 bg-gradient-to-b from-[#FF781F]/40 via-[#A855F7]/20 to-transparent shadow-2xl">
          <div className="w-full h-96 rounded-[22px] bg-[#0c0817] border border-[#261d3b] relative overflow-hidden flex items-center justify-center">
            {/* Ambient Background Contours */}
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-orange-500/10 via-purple-900/10 to-transparent" />

            {/* Glowing Center Core */}
            <div className="relative z-10 flex flex-col items-center">
              <div className="w-28 h-28 rounded-3xl bg-gradient-to-tr from-[#FF781F] to-[#A855F7] p-1 shadow-2xl shadow-orange-500/40 animate-pulse-slow">
                <div className="w-full h-full bg-[#150d28] rounded-[20px] flex flex-col items-center justify-center text-center p-3">
                  <Activity className="w-8 h-8 text-[#FF781F] mb-1" />
                  <span className="text-xs font-bold text-white">Central Hub</span>
                  <span className="text-[9px] text-[#20E88A] font-mono">10 Gbps Mesh</span>
                </div>
              </div>
            </div>

            {/* Outer Satellites */}
            <div className="absolute left-[18%] top-[30%] p-3 rounded-2xl bg-[#160f2a] border border-[#20E88A] shadow-xl text-center">
              <Server className="w-5 h-5 text-[#20E88A] mx-auto mb-1" />
              <span className="text-[10px] font-bold text-white">Core Switch 01</span>
              <p className="text-[9px] text-[#20E88A]">Healthy (4ms)</p>
            </div>

            <div className="absolute right-[18%] top-[30%] p-3 rounded-2xl bg-[#160f2a] border border-[#20D9FF] shadow-xl text-center">
              <Radio className="w-5 h-5 text-[#20D9FF] mx-auto mb-1" />
              <span className="text-[10px] font-bold text-white">Access Point Mesh</span>
              <p className="text-[9px] text-[#20D9FF]">Wi-Fi 6 Online</p>
            </div>

            <div className="absolute left-[26%] bottom-[20%] p-3 rounded-2xl bg-[#160f2a] border border-[#FF4568] shadow-xl text-center">
              <AlertTriangle className="w-5 h-5 text-[#FF4568] mx-auto mb-1" />
              <span className="text-[10px] font-bold text-white">Building A Uplink</span>
              <p className="text-[9px] text-[#FF4568]">Degraded (240ms)</p>
            </div>

            <div className="absolute right-[26%] bottom-[20%] p-3 rounded-2xl bg-[#160f2a] border border-[#A855F7] shadow-xl text-center">
              <Cpu className="w-5 h-5 text-[#A855F7] mx-auto mb-1" />
              <span className="text-[10px] font-bold text-white">Core DNS/DHCP</span>
              <p className="text-[9px] text-[#A855F7]">Active (99.9%)</p>
            </div>
          </div>
        </div>
      </section>

      {/* 5 Specialized Diagnostic Agents Section */}
      <section id="agents" className="relative z-10 max-w-7xl mx-auto px-6 py-20 border-t border-[#1e172e]">
        <div className="text-center max-w-3xl mx-auto mb-14">
          <span className="text-xs font-bold text-[#A855F7] uppercase tracking-widest">Multi-Agent Intelligence</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white mt-2">Five Specialized Autonomous Diagnostic Agents</h2>
          <p className="text-xs sm:text-sm text-[#A9A3B8] mt-3">
            Each agent investigates distinct network layers through deterministic analysis and specialized ML inference.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {[
            {
              name: 'Performance Agent',
              color: '#A855F7',
              icon: Zap,
              desc: 'Analyzes latency, jitter, packet loss, bandwidth utilization and queue drops.'
            },
            {
              name: 'Infrastructure Health Agent',
              color: '#20E88A',
              icon: Cpu,
              desc: 'Monitors CPU, memory, chassis thermal state and interface CRC counters.'
            },
            {
              name: 'Connectivity Agent',
              color: '#20D9FF',
              icon: Radio,
              desc: 'Evaluates DNS resolution, DHCP delay, gateway reachability, and 802.11 signal.'
            },
            {
              name: 'Fault Correlation Agent',
              color: '#E040FB',
              icon: GitBranch,
              desc: 'Central fusion brain that weights cross-agent evidence and resolves conflicting signals.'
            },
            {
              name: 'Recommendation Agent',
              color: '#FF9B35',
              icon: FileCheck2,
              desc: 'Generates explainable diagnostic reports, confidence metrics, and remediations.'
            }
          ].map((agent, i) => {
            const Icon = agent.icon;
            return (
              <div
                key={i}
                className="glass-panel rounded-2xl p-5 flex flex-col justify-between hover:border-[#FF781F]/40 transition-all group"
              >
                <div>
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-lg"
                    style={{ backgroundColor: `${agent.color}22` }}
                  >
                    <Icon className="w-6 h-6" style={{ color: agent.color }} />
                  </div>
                  <h3 className="text-sm font-bold text-white mb-2">{agent.name}</h3>
                  <p className="text-xs text-[#A9A3B8] leading-relaxed">{agent.desc}</p>
                </div>
                <div className="pt-4 mt-4 border-t border-[#261d3b] flex items-center gap-1.5 text-[10px] font-semibold" style={{ color: agent.color }}>
                  <span>NetCoop Agent Node</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Four ML Intelligence Modules Section */}
      <section id="models" className="relative z-10 max-w-7xl mx-auto px-6 py-20 border-t border-[#1e172e]">
        <div className="text-center max-w-3xl mx-auto mb-14">
          <span className="text-xs font-bold text-[#FF781F] uppercase tracking-widest">Trained Intelligence</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white mt-2">Four Machine Learning Models</h2>
          <p className="text-xs sm:text-sm text-[#A9A3B8] mt-3">
            Genuinely trained on reproducible multi-incident synthetic datasets and integrated into live inference pipelines.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              name: 'Isolation Forest',
              type: 'Anomaly Detection',
              metric: 'Precision / Recall',
              desc: 'Identifies multi-metric telemetry outliers and uncharacteristic performance deviations.'
            },
            {
              name: 'XGBoost Classifier',
              type: 'Fault Classification',
              metric: '7 Fault Classes',
              desc: 'Distinguishes congestion, hardware failures, Wi-Fi issues, DNS faults and latency spikes.'
            },
            {
              name: 'Random Forest',
              type: 'Infrastructure Health',
              metric: 'Feature Importance',
              desc: 'Classifies CPU starvation, memory saturation, buffer congestion, and CRC physical errors.'
            },
            {
              name: 'Gradient Boosting',
              type: 'Health Classification',
              metric: 'Tri-State Severity',
              desc: 'Categorizes network segment state into Healthy, Warning, and Critical alerts.'
            }
          ].map((mod, i) => (
            <div key={i} className="glass-panel rounded-2xl p-5 border-t-2 border-t-[#FF781F]">
              <span className="text-[10px] font-bold text-[#FF9B35] uppercase tracking-wider">{mod.type}</span>
              <h3 className="text-base font-bold text-white mt-1 mb-2">{mod.name}</h3>
              <p className="text-xs text-[#A9A3B8] leading-relaxed mb-4">{mod.desc}</p>
              <div className="p-2 rounded-lg bg-[#140c24] border border-[#2b1f44] text-[10px] font-mono text-[#20D9FF]">
                Active Inference Ready
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-[#1e172e] py-10 px-6 text-center text-xs text-[#7e7494]">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-[#FF781F]" />
            <span className="font-bold text-white">NETCOOP AI</span>
            <span>— Multi-Agent Network Fault Diagnosis Platform</span>
          </div>
          <p>© 2026 NetCoop AI. Built for Final-Round Hackathon Demonstration.</p>
        </div>
      </footer>
    </div>
  );
};
