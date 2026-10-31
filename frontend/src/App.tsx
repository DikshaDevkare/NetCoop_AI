import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { Dashboard } from './pages/Dashboard';
import { NewDiagnosis } from './pages/NewDiagnosis';
import { IncidentDetails } from './pages/IncidentDetails';
import { AgentMonitor } from './pages/AgentMonitor';
import { DiagnosisReport } from './pages/DiagnosisReport';
import { IncidentHistory } from './pages/IncidentHistory';
import { InteroperabilityLab } from './pages/InteroperabilityLab';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Landing & Authentication */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* 7 Core Application Pages */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/new-diagnosis" element={<NewDiagnosis />} />
        <Route path="/incidents/:id" element={<IncidentDetails />} />
        <Route path="/agent-monitor" element={<AgentMonitor />} />
        <Route path="/diagnosis-report/:id" element={<DiagnosisReport />} />
        <Route path="/incident-history" element={<IncidentHistory />} />
        <Route path="/interoperability-lab" element={<InteroperabilityLab />} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
