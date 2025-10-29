const API_BASE = "http://127.0.0.1:5001"; // change to your Render URL after deploy

export async function fetchTours(params = {}) {
  const usp = new URLSearchParams(params).toString();
  const res = await fetch(`${API_BASE}/api/tours?${usp}`);
  return res.json();
}

export async function fetchDestinations() {
  const res = await fetch("data/tours.json"); // static fallback for cards
  return res.json();
}

export async function fetchFAQ() {
  const res = await fetch("data/faq.json");
  return res.json();
}

export async function chatAsk(message) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ message })
  });
  return res.json();
}

export async function createBooking(payload) {
  const res = await fetch(`${API_BASE}/api/bookings`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });
  return res.json();
}
