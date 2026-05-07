// ── Navbar scroll effect ──────────────────────────────
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNav');
  if (!nav) return;
  if (window.scrollY > 50) {
    nav.style.background = 'rgba(26,5,51,1)';
    nav.style.boxShadow = '0 4px 24px rgba(0,0,0,.3)';
  } else {
    nav.style.background = 'rgba(26,5,51,.95)';
    nav.style.boxShadow = 'none';
  }
});

// ── Time ago helper ───────────────────────────────────
function timeAgo(isoStr) {
  const diff = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60)  return mins <= 1 ? 'Just now' : `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs  < 24)  return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

// ── Animate time badges ───────────────────────────────
document.querySelectorAll('[data-posted]').forEach(el => {
  el.textContent = timeAgo(el.dataset.posted);
});

// ── Admin: scrape jobs ────────────────────────────────
const scrapeBtn = document.getElementById('scrapeBtn');
if (scrapeBtn) {
  scrapeBtn.addEventListener('click', async () => {
    scrapeBtn.disabled = true;
    scrapeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>Scraping…';
    try {
      const res  = await fetch('/api/scrape', { method: 'POST' });
      const data = await res.json();
      showToast(`${data.added} new jobs scraped successfully!`, 'success');
      setTimeout(() => location.reload(), 1500);
    } catch {
      showToast('Scrape failed. Try again.', 'error');
    } finally {
      scrapeBtn.disabled = false;
      scrapeBtn.innerHTML = '<i class="fa-solid fa-rotate me-2"></i>Scrape New Jobs';
    }
  });
}

// ── Toast notifications ───────────────────────────────
function showToast(msg, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast-notif toast-${type}`;
  toast.innerHTML = `<i class="fa-solid fa-${type === 'success' ? 'circle-check' : 'circle-xmark'} me-2"></i>${msg}`;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 400); }, 3500);
}

// ── Admin delete confirm ──────────────────────────────
document.querySelectorAll('.btn-delete-job').forEach(btn => {
  btn.addEventListener('click', e => {
    if (!confirm('Delete this job listing permanently?')) e.preventDefault();
  });
});

// ── Smooth counter animation ──────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  let curr = 0;
  const step = Math.ceil(target / 60);
  const timer = setInterval(() => {
    curr = Math.min(curr + step, target);
    el.textContent = curr.toLocaleString();
    if (curr >= target) clearInterval(timer);
  }, 20);
}

const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { animateCounter(e.target); io.unobserve(e.target); } });
}, { threshold: .5 });

document.querySelectorAll('[data-target]').forEach(el => io.observe(el));
