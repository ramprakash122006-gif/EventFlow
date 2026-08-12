import React, { useState, useEffect, useMemo } from 'react';
import { Header } from './components/Header';
import { EventCard } from './components/EventCard';
import { RegistrationModal } from './components/RegistrationModal';
import { RegistrationsListModal } from './components/RegistrationsListModal';
import { Toast } from './components/Toast';
import { eventApi } from './services/api';
import { Plus, RefreshCw, AlertCircle } from 'lucide-react';

export default function App() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');

  const [registerEvent, setRegisterEvent] = useState(null);
  const [attendeesEvent, setAttendeesEvent] = useState(null);
  const [toast, setToast] = useState(null);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await eventApi.getEvents();
      setEvents(data);
    } catch (err) {
      setError(err.message || 'Failed to load events from backend server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const totalSeats = useMemo(() => {
    return events.reduce((sum, e) => sum + e.total_capacity, 0);
  }, [events]);

  const filteredEvents = useMemo(() => {
    if (filter === 'available') {
      return events.filter((e) => e.available_seats > 0);
    }
    if (filter === 'full') {
      return events.filter((e) => e.is_full);
    }
    return events;
  }, [events, filter]);

  const handleRegistrationSuccess = (registration) => {
    const isConfirmed = registration.status === 'CONFIRMED';
    setToast({
      type: 'success',
      message: isConfirmed
        ? 'Successfully registered!'
        : 'Added to waitlist!',
    });
    fetchEvents();
  };


  return (
    <>
      <Header totalEvents={events.length} totalSeats={totalSeats} />

      <main className="container">
        <div className="controls-bar">
          <div className="tab-group">
            <button
              className={`tab-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
              id="filter-all-btn"
            >
              All Events ({events.length})
            </button>
            <button
              className={`tab-btn ${filter === 'available' ? 'active' : ''}`}
              onClick={() => setFilter('available')}
              id="filter-available-btn"
            >
              Seats Available ({events.filter((e) => e.available_seats > 0).length})
            </button>
            <button
              className={`tab-btn ${filter === 'full' ? 'active' : ''}`}
              onClick={() => setFilter('full')}
              id="filter-full-btn"
            >
              Waitlist Only ({events.filter((e) => e.is_full).length})
            </button>
          </div>

          <button className="btn-secondary" onClick={fetchEvents} id="refresh-events-btn">
            <RefreshCw size={16} /> Refresh
          </button>
        </div>

        {error && (
          <div className="alert-box alert-danger" style={{ marginBottom: '2rem' }}>
            <AlertCircle size={20} />
            <div>
              <strong>Backend Connection Issue:</strong> {error}
              <p style={{ marginTop: '4px', fontSize: '0.85rem' }}>Make sure the FastAPI backend is running on <code>http://127.0.0.1:8000</code>.</p>
            </div>
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem 0', color: '#94a3b8' }}>
            <RefreshCw size={32} className="spin" style={{ marginBottom: '1rem', color: '#6366f1' }} />
            <p style={{ fontSize: '1.1rem', fontWeight: '500' }}>Fetching real-time event capacity...</p>
          </div>
        ) : filteredEvents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '4rem 0', color: '#64748b' }}>
            <p style={{ fontSize: '1.1rem' }}>No events match the selected filter.</p>
          </div>
        ) : (
          <div className="events-grid">
            {filteredEvents.map((event) => (
              <EventCard
                key={event.id}
                event={event}
                onRegister={(ev) => setRegisterEvent(ev)}
                onViewAttendees={(ev) => setAttendeesEvent(ev)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Modals */}
      {registerEvent && (
        <RegistrationModal
          event={registerEvent}
          onClose={() => setRegisterEvent(null)}
          onSuccess={handleRegistrationSuccess}
        />
      )}

      {attendeesEvent && (
        <RegistrationsListModal
          event={attendeesEvent}
          onClose={() => setAttendeesEvent(null)}
          onRefreshEvent={fetchEvents}
        />
      )}

      {/* Toast Notification */}
      <Toast toast={toast} onClose={() => setToast(null)} />
    </>
  );
}
