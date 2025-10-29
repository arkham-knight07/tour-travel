import { fetchTours, fetchDestinations, fetchFAQ } from "./api.js";

const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Render Deals (from backend if running; else static file fallback)
async function renderDeals() {
  const grid = document.getElementById("dealsGrid");
  if (!grid) return;
  try {
    const tours = await fetchTours({ featured: 1 });
    grid.innerHTML = tours.map(cardHTML).join("");
  } catch {
    const data = await fetchDestinations();
    grid.innerHTML = data.filter(t=>t.featured).map(cardHTML).join("");
  }
}

// Render Destinations
async function renderDestinations() {
  const grid = document.getElementById("destGrid");
  if (!grid) return;
  const data = await fetchDestinations();
  grid.innerHTML = data.slice(0,6).map(cardHTML).join("");
}

// Card HTML
function cardHTML(t) {
  // Choose icon based on type/category
  let icon = '';
  if (t.type === 'flight') icon = '<img class="icon" src="assets/images/services/flight.jpg" alt="Flight">';
  else if (t.type === 'hotel') icon = '<img class="icon" src="assets/images/services/hotel.jpg" alt="Hotel">';
  else if (t.type === 'bus') icon = '<img class="icon" src="assets/images/services/bus.jpg" alt="Bus">';
  else if (t.type === 'train') icon = '<img class="icon" src="assets/images/services/train.jpg" alt="Train">';
  else if (t.type === 'trek') icon = '<img class="icon" src="assets/images/services/trek.jpg" alt="Trek">';
  else if (t.type === 'international') icon = '<img class="icon" src="assets/images/services/international.jpg" alt="International">';
  return `
  <article class="card fade-in" tabindex="0">
    <img src="${t.image}" alt="${t.title}" loading="lazy">
    ${icon}
    <div class="p">
      <h3>${t.title}</h3>
      <p>${t.short || ""}</p>
      <p class="price">${t.currency || "₹"}${t.price}</p>
      <a class="btn" href="pages/booking.html?tour=${encodeURIComponent(t.id)}">Book</a>
    </div>
  </article>`;
}

// Search form
const sf = document.getElementById("searchForm");
sf?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = document.getElementById("q").value.trim();
  const type = document.getElementById("type").value;
  const grid = document.getElementById("destGrid");
  grid.innerHTML = "<p>Searching…</p>";
  const tours = await fetchTours({ q, type });
  grid.innerHTML = tours.length ? tours.map(cardHTML).join("") : "<p>No results.</p>";
});

// FAQ
async function renderFAQ(){
  const wrap = document.getElementById("faqList");
  if (!wrap) return;
  const faq = await fetchFAQ();
  wrap.innerHTML = Object.entries(faq).map(([k,v],i)=>
    `<details class="faq-item fade-in"${i===0?' open':''}><summary>${cap(k)}</summary><div>${v}</div></details>`
  ).join("");
  // Animate FAQ open/close
  wrap.querySelectorAll('details').forEach(d => {
    d.addEventListener('toggle', function() {
      if(this.open) this.classList.add('active');
      else this.classList.remove('active');
    });
  });
}
const cap = s => s.charAt(0).toUpperCase()+s.slice(1);

// PWA
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/service-worker.js").catch(console.warn);
}

renderDeals();
renderDestinations();
renderFAQ();
