import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { LivingBackground } from './LivingBackground';

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children, title, subtitle }) => {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#070711] text-[#F5F2FA]">
      <LivingBackground />
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative z-10">
        <Header title={title} subtitle={subtitle} />
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
};
