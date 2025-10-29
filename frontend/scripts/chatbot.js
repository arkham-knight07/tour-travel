import { chatAsk } from "./api.js";

const chatBtn = document.getElementById('chatButton');
const chatWin = document.getElementById('chatWindow');
const chatClose = document.getElementById('chatClose');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');

// Simple FAQ responses (fallback if API fails)
const simpleFAQ = {
  'booking': 'Go to a package and click Book. Fill your details and confirm.',
  'payment': 'We accept UPI, cards, and PayPal. You\'ll receive an email invoice.',
  'refund': 'Refunds are processed within 5–7 business days after approval.',
  'cancellation': 'Cancel up to 7 days before departure for a full refund.',
  'visa': 'International packages include visa guidance and document checklist.',
  'support': 'Reach us at support@travelmate.com or +91-9876543210.'
};


// Accessibility: focus input when chat opens
chatBtn.addEventListener('click', () => {
  chatWin.classList.toggle('hidden');
  if (!chatWin.classList.contains('hidden')) setTimeout(()=>chatInput.focus(), 200);
});
chatClose.addEventListener('click', () => chatWin.classList.add('hidden'));
chatSend.addEventListener('click', handleSend);
chatInput.addEventListener('keydown', e => { if (e.key === 'Enter') handleSend(); });

// Quick reply buttons
const quickReplies = [
  { text: 'How to book?', emoji: '📝' },
  { text: 'Refund policy', emoji: '💸' },
  { text: 'Popular tours', emoji: '🌍' },
  { text: 'Visa help', emoji: '🛂' }
];
function renderQuickReplies() {
  const qrDiv = document.createElement('div');
  qrDiv.className = 'quick-replies';
  quickReplies.forEach(q => {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.type = 'button';
    btn.textContent = `${q.emoji} ${q.text}`;
    btn.style.margin = '4px 6px 0 0';
    btn.onclick = () => {
      chatInput.value = q.text;
      handleSend();
    };
    qrDiv.appendChild(btn);
  });
  chatBody.appendChild(qrDiv);
}

function addMsg(text, who='bot', isLoading=false){
  const d = document.createElement('div');
  d.className = `msg ${who}`;
  if(isLoading) {
    d.innerHTML = '<span class="dot-flashing"></span>';
    d.setAttribute('aria-label', 'Loading');
  } else {
    // Emoji support
    d.innerHTML = text.replace(/\n/g, '<br>')
      .replace(/:([a-z_]+):/g, (m, code) => emojiMap[code] || m);
  }
  chatBody.appendChild(d);
  chatBody.scrollTop = chatBody.scrollHeight;
  return d;
}

// Emoji map for basic support
const emojiMap = {
  smile: '😊',
  book: '📖',
  refund: '💸',
  world: '🌍',
  visa: '🛂',
  check: '✅',
  cross: '❌',
  info: 'ℹ️',
};

async function handleSend(){
  const text = chatInput.value.trim();
  if (!text) return;
  chatInput.value = '';
  addMsg(text, 'user');
  const loadingMsg = addMsg('', 'bot', true);
  
  // Try API first, fallback to simple FAQ
  try{
    const { reply } = await chatAsk(text);
    loadingMsg.remove();
    addMsg(reply || getFallbackResponse(text));
  } catch {
    loadingMsg.remove();
    addMsg(getFallbackResponse(text));
  }
}

function getFallbackResponse(message) {
  const msg = message.toLowerCase();
  
  // Check for exact matches first
  for (const [key, response] of Object.entries(simpleFAQ)) {
    if (msg.includes(key)) {
      return response;
    }
  }
  
  // Default response
  return "I can help with booking, payment, refund, cancellation, or visa questions. What would you like to know?";
}

// Add a simple loading animation style
const style = document.createElement('style');
style.textContent = `
.dot-flashing {
  position: relative;
  width: 16px;
  height: 8px;
}
.dot-flashing::before, .dot-flashing::after, .dot-flashing {
  content: '';
  display: inline-block;
  border-radius: 50%;
  width: 8px;
  height: 8px;
  background: var(--primary, #ff6a3d);
  margin: 0 1px;
  animation: dotFlashing 1s infinite linear alternate;
}
.dot-flashing::before {
  animation-delay: 0s;
}
.dot-flashing {
  animation-delay: 0.3s;
}
.dot-flashing::after {
  animation-delay: 0.6s;
}
@keyframes dotFlashing {
  0% { opacity: 0.2; }
  50%,100% { opacity: 1; }
}
`;
document.head.appendChild(style);

addMsg('Hi! I can help with booking, refund, payment, visa, or packages.');
renderQuickReplies();
// Quick reply styles
const qrStyle = document.createElement('style');
qrStyle.textContent = `
.quick-replies { display: flex; flex-wrap: wrap; gap: 0.5em; margin: 6px 0 0 0; }
.quick-replies .btn { font-size: 0.98em; padding: 7px 12px; background: var(--panel); color: var(--text); border: 1px solid var(--border); border-radius: 8px; transition: background .2s; }
.quick-replies .btn:hover { background: var(--primary); color: #fff; }
`;
document.head.appendChild(qrStyle);