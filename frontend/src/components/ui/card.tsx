import React from 'react';

export const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`shadow-lg rounded-xl overflow-hidden ${className}`}>{children}</div>
);

export const CardContent = ({ children }: { children: React.ReactNode }) => (
  <div className="p-4">{children}</div>
);
