import React from 'react';
import { CheckCircle, AlertTriangle, Clock } from 'lucide-react';

export function CapacityBadge({ availableSeats, isFull }) {
  if (isFull) {
    return (
      <span className="badge badge-full">
        <Clock size={12} />
        Waitlist Only
      </span>
    );
  }

  if (availableSeats <= 2) {
    return (
      <span className="badge badge-limited">
        <AlertTriangle size={12} />
        {availableSeats} {availableSeats === 1 ? 'Seat Left' : 'Seats Left'}
      </span>
    );
  }

  return (
    <span className="badge badge-available">
      <CheckCircle size={12} />
      {availableSeats} Seats Available
    </span>
  );
}
