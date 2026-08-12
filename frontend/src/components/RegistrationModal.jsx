import React, { useState } from 'react';
import { X, AlertCircle, CheckCircle, Clock, Send } from 'lucide-react';
import { eventApi } from '../services/api';

export function RegistrationModal({ event, onClose, onSuccess }) {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [statusResult, setStatusResult] = useState(null);

  if (!event) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setStatusResult(null);

    if (!fullName.trim() || !email.trim()) {
      setError('Please provide both your full name and email address.');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      setError('Please enter a valid email address (e.g. user@example.com).');
      return;
    }


    try {
      setLoading(true);
      const registration = await eventApi.registerForEvent(event.id, {
        full_name: fullName.trim(),
        email: email.trim(),
      });
      setStatusResult(registration);
      onSuccess(registration, event);
    } catch (err) {
      setError(err.message || 'Failed to submit registration.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()} id="registration-modal">
        <div className="modal-header">
          <div>
            <h3 className="modal-title">Event Registration</h3>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{event.title}</p>
          </div>
          <button className="modal-close" onClick={onClose} id="close-modal-btn">
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          {error && (
            <div className="alert-box alert-danger" id="registration-error-alert">
              <AlertCircle size={18} style={{ flexShrink: 0 }} />
              <div>{error}</div>
            </div>
          )}

          {statusResult ? (
            <div className="alert-box alert-success" id="registration-success-alert">
              {statusResult.status === 'CONFIRMED' ? (
                <CheckCircle size={20} style={{ flexShrink: 0 }} />
              ) : (
                <Clock size={20} style={{ flexShrink: 0 }} />
              )}
              <div>
                <strong style={{ display: 'block', fontSize: '1rem', marginBottom: '4px' }}>
                  {statusResult.status === 'CONFIRMED'
                    ? 'Successfully registered!'
                    : 'Added to Waitlist!'}
                </strong>
                {statusResult.status === 'CONFIRMED'
                  ? `Your seat has been reserved for ${statusResult.email}.`
                  : `Capacity is currently full. ${statusResult.email} has been placed on the priority waitlist.`}

              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} noValidate>
              <div className="form-group">

                <label className="form-label" htmlFor="full_name">Full Name</label>
                <input
                  id="full_name"
                  type="text"
                  className="form-input"
                  placeholder="e.g. John Doe"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="email">Email Address</label>
                <input
                  id="email"
                  type="email"
                  className="form-input"
                  placeholder="e.g. john.doe@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
                <button type="button" className="btn-secondary" onClick={onClose} disabled={loading}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={loading} id="submit-registration-btn">
                  {loading ? 'Processing...' : (
                    <>
                      <Send size={16} /> Submit Registration
                    </>
                  )}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
