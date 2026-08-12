const API_BASE = '/api/v1';

async function handleResponse(response) {
  const contentType = response.headers.get('content-type');
  let data = null;

  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  }

  if (!response.ok) {
    let errorMsg = `HTTP Error ${response.status}: ${response.statusText}`;
    if (typeof data?.detail === 'string') {
      errorMsg = data.detail;
    } else if (Array.isArray(data?.detail)) {
      errorMsg = data.detail.map((err) => err.msg || err.detail || JSON.stringify(err)).join(' ');
    }

    const error = new Error(errorMsg);
    error.status = response.status;
    error.errorCode = data?.error_code || 'API_ERROR';
    throw error;
  }

  return data;
}

export const eventApi = {
  // Fetch all events
  async getEvents() {
    const res = await fetch(`${API_BASE}/events`);
    return handleResponse(res);
  },

  // Fetch single event details
  async getEventDetail(id) {
    const res = await fetch(`${API_BASE}/events/${id}`);
    return handleResponse(res);
  },

  // Register attendee for event
  async registerForEvent(eventId, payload) {
    const res = await fetch(`${API_BASE}/events/${eventId}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  // Create new event (admin / demo helper)
  async createEvent(payload) {
    const res = await fetch(`${API_BASE}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  // Cancel registration
  async cancelRegistration(registrationId) {
    const res = await fetch(`${API_BASE}/registrations/${registrationId}/cancel`, {
      method: 'POST',
    });
    return handleResponse(res);
  },
};
