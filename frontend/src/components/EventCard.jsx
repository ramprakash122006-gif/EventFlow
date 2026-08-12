import React from 'react';
import { MapPin, Calendar, Users, UserCheck, Clock } from 'lucide-react';
import { CapacityBadge } from './CapacityBadge';

export function EventCard({ event, onRegister, onViewAttendees }) {
  const { id, title, description, location, start_time, total_capacity, confirmed_count, waitlisted_count, available_seats, is_full } = event;

  const percentage = Math.min(100, Math.round((confirmed_count / total_capacity) * 100));

  let fillClass = 'fill-available';
  if (is_full) {
    fillClass = 'fill-full';
  } else if (percentage >= 70) {
    fillClass = 'fill-limited';
  }

  const formattedDate = new Date(start_time).toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });

  const isPast = new Date(start_time) < new Date();

  return (
    <div className="event-card" id={`event-card-${id}`}>
      <div>
        <div className="card-header">
          <h2 className="event-title">{title}</h2>
          <CapacityBadge availableSeats={available_seats} isFull={is_full} />
        </div>

        <p className="event-description">{description || 'Join us for this exciting live event.'}</p>

        <div className="meta-group">
          <div className="meta-item">
            <Calendar size={15} style={{ color: '#06b6d4' }} />
            <span>{formattedDate}</span>
          </div>
          <div className="meta-item">
            <MapPin size={15} style={{ color: '#a855f7' }} />
            <span>{location}</span>
          </div>
        </div>
      </div>

      <div>
        <div className="capacity-section">
          <div className="capacity-header">
            <span className="capacity-title">Seat Availability</span>
            <span className="capacity-seats">
              <strong style={{ color: is_full ? '#a855f7' : '#10b981' }}>{confirmed_count}</strong> / {total_capacity} confirmed
              {waitlisted_count > 0 && <span style={{ color: '#f59e0b', marginLeft: '6px' }}>({waitlisted_count} waitlisted)</span>}
            </span>
          </div>

          <div className="progress-bar-bg">
            <div
              className={`progress-bar-fill ${fillClass}`}
              style={{ width: `${percentage}%` }}
            ></div>
          </div>
        </div>

        <div className="card-actions">
          <button
            className="btn-primary"
            style={{ flex: 1, opacity: isPast ? 0.6 : 1 }}
            disabled={isPast}
            onClick={() => onRegister(event)}
            id={`register-btn-${id}`}
          >
            {isPast ? (
              'Past Event'
            ) : is_full ? (
              <>
                <Clock size={16} /> Join Waitlist
              </>
            ) : (
              <>
                <UserCheck size={16} /> Register Now
              </>
            )}
          </button>

          <button
            className="btn-secondary"
            onClick={() => onViewAttendees(event)}
            id={`view-attendees-btn-${id}`}
            title="View attendee list and manage registrations"
          >
            <Users size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
