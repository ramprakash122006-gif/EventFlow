import React, { useState, useEffect } from 'react';
import { X, Trash2, CheckCircle, Clock, Ban, RefreshCw } from 'lucide-react';
import { eventApi } from '../services/api';

export function RegistrationsListModal({ event, onClose, onRefreshEvent }) {
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [cancellingId, setCancellingId] = useState(null);

  const fetchRegistrations = async () => {
    if (!event) return;
    try {
      setLoading(true);
      setError('');
      const detail = await eventApi.getEventDetail(event.id);
      setRegistrations(detail.registrations || []);
    } catch (err) {
      setError(err.message || 'Failed to load attendees.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRegistrations();
  }, [event]);

  const handleCancel = async (regId) => {
    try {
      setCancellingId(regId);
      await eventApi.cancelRegistration(regId);
      await fetchRegistrations();
      if (onRefreshEvent) onRefreshEvent();
    } catch (err) {
      setError(err.message || 'Failed to cancel registration.');
    } finally {
      setCancellingId(null);
    }
  };

  if (!event) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" style={{ maxWidth: '640px' }} onClick={(e) => e.stopPropagation()} id="attendees-modal">
        <div className="modal-header">
          <div>
            <h3 className="modal-title">Event Attendees & Waitlist</h3>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{event.title}</p>
          </div>
          <button className="modal-close" onClick={onClose} id="close-attendees-modal-btn">
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          {error && (
            <div className="alert-box alert-danger">
              <div>{error}</div>
            </div>
          )}

          {loading ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
              <RefreshCw size={24} className="spin" style={{ marginBottom: '0.5rem' }} />
              <p>Loading attendees list...</p>
            </div>
          ) : registrations.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2.5rem', color: '#64748b' }}>
              <p>No registrations found for this event yet.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxHeight: '360px', overflowY: 'auto' }}>
              {registrations.map((reg) => (
                <div
                  key={reg.id}
                  style={{
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--surface-border)',
                    padding: '0.875rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                  id={`attendee-item-${reg.id}`}
                >
                  <div>
                    <div style={{ fontWeight: '600', color: '#f8fafc' }}>{reg.full_name}</div>
                    <div style={{ fontSize: '0.825rem', color: '#94a3b8' }}>{reg.email}</div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    {reg.status === 'CONFIRMED' && (
                      <span className="badge badge-available">
                        <CheckCircle size={12} /> Confirmed
                      </span>
                    )}
                    {reg.status === 'WAITLISTED' && (
                      <span className="badge badge-full">
                        <Clock size={12} /> Waitlist
                      </span>
                    )}
                    {reg.status === 'CANCELLED' && (
                      <span className="badge" style={{ background: 'rgba(100, 116, 139, 0.2)', color: '#94a3b8' }}>
                        <Ban size={12} /> Cancelled
                      </span>
                    )}

                    {reg.status !== 'CANCELLED' && (
                      <button
                        className="btn-secondary"
                        style={{ padding: '0.4rem 0.6rem', color: '#f43f5e' }}
                        title="Cancel Registration"
                        onClick={() => handleCancel(reg.id)}
                        disabled={cancellingId === reg.id}
                        id={`cancel-reg-btn-${reg.id}`}
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
