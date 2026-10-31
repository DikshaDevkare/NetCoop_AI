import React, { useState } from 'react';
import { AppLayout } from '../components/layout/AppLayout';
import { api } from '../services/api';
import {
  Layers,
  CheckCircle2,
  XCircle,
  Send,
  Check,
  AlertTriangle,
  Code2,
  RefreshCw,
  Terminal,
  Sparkles
} from 'lucide-react';

export const InteroperabilityLab: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'Message Builder' | 'Compatibility Test' | 'Schema' | 'Logs'>('Message Builder');
  const [protocol, setProtocol] = useState('NetCoop Agent v1.0');
  const [messageType, setMessageType] = useState('diagnosis_request');
  const [schemaVersion, setSchemaVersion] = useState('v1.0.0');

  const defaultJSON = JSON.stringify(
    {
      message_id: 'msg-7042',
      sender: 'orchestrator',
      receiver: 'performance_agent',
      type: 'diagnosis_request',
      message_type: 'diagnosis_request',
      schema_version: '1.0',
      payload: {
        incident_id: 'INC-1024',
        telemetry_window: '15m',
        metric: 'latency_ms',
        value: 240,
        unit: 'ms'
      }
    },
    null,
    2
  );

  const [jsonText, setJsonText] = useState(defaultJSON);
  const [validationResult, setValidationResult] = useState<any>({
    schema_valid: true,
    required_fields_present: true,
    data_types_correct: true,
  });
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [isValidating, setIsValidating] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const [exchangeLogs, setExchangeLogs] = useState<any[]>([
    { from: 'Orchestrator', to: 'Perf Agent', time: '14:02:11', status: 'delivered' },
    { from: 'Perf Agent', to: 'Orchestrator', time: '14:02:14', status: 'acknowledged' },
    { from: 'Orchestrator', to: 'Corr Agent', time: '14:02:20', status: 'routed' },
  ]);

  const handleValidate = async () => {
    try {
      setIsValidating(true);
      setValidationErrors([]);
      setStatusMessage('');

      let parsed: any;
      try {
        parsed = JSON.parse(jsonText);
      } catch (e: any) {
        setValidationResult({
          schema_valid: false,
          required_fields_present: false,
          data_types_correct: false,
        });
        setValidationErrors([`Invalid JSON syntax: ${e.message}`]);
        return;
      }

      const res = await api.validateProtocolMessage(parsed);
      setValidationResult(res.checks || {});
      setValidationErrors(res.errors || []);
      if (res.is_valid) {
        setStatusMessage('Message adheres 100% to NetCoop Agent Protocol.');
      }
    } catch (err: any) {
      console.error(err);
      setValidationErrors(['Gateway validation service offline.']);
    } finally {
      setIsValidating(false);
    }
  };

  const handleSend = async () => {
    try {
      setIsValidating(true);
      const parsed = JSON.parse(jsonText);
      const res = await api.sendTestMessage(parsed);
      if (res.checks) setValidationResult(res.checks);
      if (res.errors) setValidationErrors(res.errors);
      if (res.exchange_log) {
        const newLogs = res.exchange_log.map((l: any) => ({
          from: l.sender,
          to: l.receiver,
          time: l.time,
          status: l.status,
        }));
        setExchangeLogs((prev) => [...newLogs, ...prev].slice(0, 6));
      }
      setStatusMessage(res.message || 'Dispatched across agent message bus.');
    } catch (e: any) {
      setValidationErrors([`Failed to send: ${e.message}`]);
    } finally {
      setIsValidating(false);
    }
  };

  // Test Presets
  const loadPreset = (type: string) => {
    if (type === 'valid_finding') {
      setJsonText(
        JSON.stringify(
          {
            message_id: 'MSG-001',
            incident_id: 'INC-1024',
            sender: 'performance_agent',
            receiver: 'fault_correlation_agent',
            message_type: 'diagnostic_finding',
            schema_version: '1.0',
            payload: {
              finding: 'high_network_latency',
              metric: 'latency_ms',
              value: 280,
              unit: 'ms',
              device_id: 'HOSTEL_CORE_SW_01',
              evidence: ['Latency exceeds configured threshold']
            }
          },
          null,
          2
        )
      );
    } else if (type === 'missing_fields') {
      setJsonText(
        JSON.stringify(
          {
            sender: 'performance_agent',
            message_type: 'diagnostic_finding',
            payload: { value: 100 }
          },
          null,
          2
        )
      );
    } else if (type === 'invalid_units') {
      setJsonText(
        JSON.stringify(
          {
            message_id: 'MSG-ERR-02',
            sender: 'performance_agent',
            receiver: 'fault_correlation_agent',
            message_type: 'diagnostic_finding',
            schema_version: '1.0',
            payload: {
              metric: 'latency_ms',
              value: 280,
              unit: 'meters_invalid'
            }
          },
          null,
          2
        )
      );
    }
  };

  return (
    <AppLayout
      title="Interoperability Lab"
      subtitle="Test agent protocols, validate messages and ensure compatibility."
    >
      {/* Tabs */}
      <div className="flex items-center justify-between border-b border-[#261d3b] pb-2">
        <div className="flex items-center gap-2">
          {(['Message Builder', 'Compatibility Test', 'Schema', 'Logs'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === tab
                  ? 'bg-[#FF781F] text-white shadow-lg shadow-orange-500/30'
                  : 'text-[#A9A3B8] hover:text-white hover:bg-[#1a122e]'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Preset Injectors */}
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-[#A9A3B8]">Test Presets:</span>
          <button
            onClick={() => loadPreset('valid_finding')}
            className="px-2 py-1 rounded bg-[#201538] hover:bg-[#20E88A]/20 text-[#20E88A] border border-[#20E88A]/40 text-[10px] font-semibold"
          >
            Valid Finding
          </button>
          <button
            onClick={() => loadPreset('missing_fields')}
            className="px-2 py-1 rounded bg-[#201538] hover:bg-[#FF4568]/20 text-[#FF4568] border border-[#FF4568]/40 text-[10px] font-semibold"
          >
            Missing Fields
          </button>
          <button
            onClick={() => loadPreset('invalid_units')}
            className="px-2 py-1 rounded bg-[#201538] hover:bg-[#FFC247]/20 text-[#FFC247] border border-[#FFC247]/40 text-[10px] font-semibold"
          >
            Incompatible Unit
          </button>
        </div>
      </div>

      {/* Main Two-Column Playground */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Dropdowns & JSON Editor */}
        <div className="glass-panel rounded-2xl p-4 space-y-4">
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">Message Builder</h4>

          {/* Config Controls */}
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-[10px] text-[#A9A3B8] block mb-1">Protocol</label>
              <select
                value={protocol}
                onChange={(e) => setProtocol(e.target.value)}
                className="w-full bg-[#140e26] border border-[#2c2047] text-white text-[11px] rounded-lg p-2 focus:border-[#FF781F]"
              >
                <option>NetCoop Agent v1.0</option>
                <option>NetCoop Telemetry v2.0</option>
              </select>
            </div>
            <div>
              <label className="text-[10px] text-[#A9A3B8] block mb-1">Message Type</label>
              <select
                value={messageType}
                onChange={(e) => setMessageType(e.target.value)}
                className="w-full bg-[#140e26] border border-[#2c2047] text-white text-[11px] rounded-lg p-2 focus:border-[#FF781F]"
              >
                <option value="diagnosis_request">diagnosis_request</option>
                <option value="diagnostic_finding">diagnostic_finding</option>
                <option value="correlation_result">correlation_result</option>
                <option value="recommendation_report">recommendation_report</option>
              </select>
            </div>
            <div>
              <label className="text-[10px] text-[#A9A3B8] block mb-1">Schema Version</label>
              <select
                value={schemaVersion}
                onChange={(e) => setSchemaVersion(e.target.value)}
                className="w-full bg-[#140e26] border border-[#2c2047] text-white text-[11px] rounded-lg p-2 focus:border-[#FF781F]"
              >
                <option>v1.0.0</option>
                <option>v1.1.0</option>
              </select>
            </div>
          </div>

          {/* JSON Editor */}
          <div>
            <label className="text-[10px] text-[#A9A3B8] block mb-1">Protocol JSON Payload</label>
            <textarea
              rows={12}
              value={jsonText}
              onChange={(e) => setJsonText(e.target.value)}
              className="w-full bg-[#0a0714] border border-[#2c2047] rounded-xl p-3 text-xs font-mono text-[#20D9FF] focus:outline-none focus:border-[#FF781F] resize-none leading-relaxed"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleValidate}
              disabled={isValidating}
              className="flex-1 py-2 rounded-xl bg-[#201538] hover:bg-[#2e1f4f] text-[#FF9B35] border border-[#FF781F]/40 font-bold text-xs flex items-center justify-center gap-1.5 transition-all shadow-md cursor-pointer"
            >
              <Check className="w-3.5 h-3.5" />
              <span>Validate</span>
            </button>
            <button
              onClick={handleSend}
              disabled={isValidating}
              className="flex-1 py-2 rounded-xl bg-gradient-to-r from-[#FF781F] to-[#FF9B35] text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 transition-all cursor-pointer"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Send Request</span>
            </button>
          </div>
        </div>

        {/* Right Column: Compatibility Results & Message Exchange Logs */}
        <div className="space-y-4">
          {/* Compatibility Results Checklist */}
          <div className="glass-panel rounded-2xl p-4">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3">Compatibility Result</h4>

            <div className="space-y-2.5">
              <div className="flex items-center gap-2.5 text-xs">
                {validationResult.schema_valid ? (
                  <CheckCircle2 className="w-4 h-4 text-[#20E88A]" />
                ) : (
                  <XCircle className="w-4 h-4 text-[#FF4568]" />
                )}
                <span className={validationResult.schema_valid ? 'text-[#20E88A]' : 'text-[#FF4568]'}>
                  Schema valid (RFC-8259 JSON & NetCoop v1.0)
                </span>
              </div>

              <div className="flex items-center gap-2.5 text-xs">
                {validationResult.required_fields_present ? (
                  <CheckCircle2 className="w-4 h-4 text-[#20E88A]" />
                ) : (
                  <XCircle className="w-4 h-4 text-[#FF4568]" />
                )}
                <span className={validationResult.required_fields_present ? 'text-[#20E88A]' : 'text-[#FF4568]'}>
                  All required fields present (message_id, sender, receiver, payload)
                </span>
              </div>

              <div className="flex items-center gap-2.5 text-xs">
                {validationResult.data_types_correct ? (
                  <CheckCircle2 className="w-4 h-4 text-[#20E88A]" />
                ) : (
                  <XCircle className="w-4 h-4 text-[#FF4568]" />
                )}
                <span className={validationResult.data_types_correct ? 'text-[#20E88A]' : 'text-[#FF4568]'}>
                  Data types & metric units correct
                </span>
              </div>
            </div>

            {/* Validation Errors Box if any */}
            {validationErrors.length > 0 && (
              <div className="mt-3 p-3 rounded-xl bg-[#280c14] border border-[#FF4568]/40 text-[#FF4568] text-xs space-y-1">
                <p className="font-bold flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" /> Validation Violations:
                </p>
                {validationErrors.map((err, i) => (
                  <p key={i} className="text-[11px] font-mono">• {err}</p>
                ))}
              </div>
            )}

            {/* Success Message */}
            {statusMessage && validationErrors.length === 0 && (
              <div className="mt-3 p-2.5 rounded-xl bg-[#0c2419] border border-[#20E88A]/40 text-[#20E88A] text-xs font-medium">
                {statusMessage}
              </div>
            )}
          </div>

          {/* Message Exchange Log */}
          <div className="glass-panel rounded-2xl p-4">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5 text-[#A855F7]" />
              <span>Message Exchange History</span>
            </h4>

            <div className="space-y-2 font-mono text-xs">
              {exchangeLogs.map((log, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2 rounded-xl bg-[#0c0817] border border-[#211636]"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-[#FF781F] font-bold">{log.from}</span>
                    <span className="text-[#7d7494]">→</span>
                    <span className="text-[#20D9FF] font-bold">{log.to}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-[#20E88A] uppercase font-semibold">{log.status}</span>
                    <span className="text-[10px] text-[#A9A3B8]">{log.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
