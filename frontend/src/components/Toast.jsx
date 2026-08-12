import React, { useEffect } from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

export function Toast({ toast, onClose }) {
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => {
      onClose();
    }, 4000);
    return () => clearTimeout(timer);
  }, [toast, onClose]);

  if (!toast) return null;

  const { type, message } = toast;

  let Icon = CheckCircle;
  let borderColor = '#10b981';

  if (type === 'error') {
    Icon = AlertCircle;
    borderColor = '#f43f5e';
  } else if (type === 'info') {
    Icon = Info;
    borderColor = '#06b6d4';
  }

  return (
    <div className="toast-container">
      <div className="toast" style={{ borderColor }} id="toast-notification">
        <Icon size={20} style={{ color: borderColor, flexShrink: 0 }} />
        <span style={{ flex: 1 }}>{message}</span>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
          <X size={16} />
        </button>
      </div>
    </div>
  );
}
