import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Interceptor to inject JWT token if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('netcoop_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Health
  getHealth: async () => {
    const res = await apiClient.get('/health');
    return res.data;
  },

  // Dashboard
  getDashboardStats: async () => {
    const res = await apiClient.get('/dashboard/stats');
    return res.data;
  },
  getDashboardTelemetry: async () => {
    const res = await apiClient.get('/dashboard/telemetry');
    return res.data;
  },
  getNetworkTopology: async () => {
    const res = await apiClient.get('/dashboard/topology');
    return res.data;
  },

  // Incidents
  getIncidents: async (params?: { severity?: string; status?: string; search?: string; limit?: number }) => {
    const res = await apiClient.get('/incidents', { params });
    return res.data;
  },
  getIncidentDetails: async (incidentId: string) => {
    const res = await apiClient.get(`/incidents/${incidentId}`);
    return res.data;
  },

  // Diagnosis
  runDiagnosis: async (payload: { scenario?: string; incident_id?: string; telemetry?: any }) => {
    const res = await apiClient.post('/diagnosis/run', payload);
    return res.data;
  },
  getDiagnosisResult: async (incidentId: string) => {
    const res = await apiClient.get(`/diagnosis/${incidentId}`);
    return res.data;
  },
  getDiagnosisReport: async (incidentId: string) => {
    const res = await apiClient.get(`/diagnosis/${incidentId}/report`);
    return res.data;
  },

  // Multi-Agent System
  getAgentsStatus: async () => {
    const res = await apiClient.get('/agents/status');
    return res.data;
  },
  getAgentMessages: async (incidentId: string) => {
    const res = await apiClient.get(`/agents/messages/${incidentId}`);
    return res.data;
  },
  getExecutionTimeline: async (incidentId: string) => {
    const res = await apiClient.get(`/agents/execution/${incidentId}`);
    return res.data;
  },

  // Interoperability Lab
  validateProtocolMessage: async (message: any) => {
    const res = await apiClient.post('/interoperability/validate', message);
    return res.data;
  },
  sendTestMessage: async (message: any) => {
    const res = await apiClient.post('/interoperability/send', message);
    return res.data;
  },
  getProtocolSchemas: async () => {
    const res = await apiClient.get('/interoperability/schemas');
    return res.data;
  },

  // ML Models
  getModelsStatus: async () => {
    const res = await apiClient.get('/models/status');
    return res.data;
  },
  getModelsMetrics: async () => {
    const res = await apiClient.get('/models/metrics');
    return res.data;
  },

  // Simulation & Scenarios
  getScenarios: async () => {
    const res = await apiClient.get('/simulation/scenarios');
    return res.data;
  },
  generateScenario: async (payload: { scenario: string; seed?: number }) => {
    const res = await apiClient.post('/simulation/generate', payload);
    return res.data;
  },
  uploadTelemetryFile: async (formData: FormData) => {
    const res = await apiClient.post('/telemetry/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  // Auth
  login: async (credentials: { email: string; password: string }) => {
    const res = await apiClient.post('/auth/login', credentials);
    if (res.data.access_token) {
      localStorage.setItem('netcoop_token', res.data.access_token);
      localStorage.setItem('netcoop_user', JSON.stringify(res.data.user));
    }
    return res.data;
  },
  register: async (data: { name: string; email: string; password: string; organization?: string; role?: string }) => {
    const res = await apiClient.post('/auth/register', data);
    if (res.data.access_token) {
      localStorage.setItem('netcoop_token', res.data.access_token);
      localStorage.setItem('netcoop_user', JSON.stringify(res.data.user));
    }
    return res.data;
  },
  logout: () => {
    localStorage.removeItem('netcoop_token');
    localStorage.removeItem('netcoop_user');
  },
  getCurrentUser: () => {
    const userStr = localStorage.getItem('netcoop_user');
    return userStr ? JSON.parse(userStr) : null;
  }
};
