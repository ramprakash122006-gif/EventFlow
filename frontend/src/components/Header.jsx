import React from 'react';
import { Calendar, Layers, ShieldCheck } from 'lucide-react';

export function Header({ totalEvents, totalSeats }) {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo-group">
            <div className="logo-icon">
              <Calendar size={24} />
            </div>
            <div>
              <h1 className="logo-title">EventFlow</h1>
              <p className="logo-subtitle">Event Registration & Capacity Management System</p>
            </div>
          </div>

          <div className="header-stats">
            <div className="stat-pill">
              <Layers size={16} style={{ color: '#06b6d4' }} />
              <span>Events: <strong>{totalEvents}</strong></span>
            </div>
            <div className="stat-pill">
              <ShieldCheck size={16} style={{ color: '#10b981' }} />
              <span>Total Capacity: <strong>{totalSeats}</strong></span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
