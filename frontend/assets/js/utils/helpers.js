export function showToast(type, msg) {
    const c = document.getElementById('toastContainer');
    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
    const d = document.createElement('div');
    d.className = `toast ${type}`;
    d.innerHTML = `<span class="toast-icon">${icons[type]}</span><span class="toast-message">${msg}</span>`;
    c.appendChild(d);
    setTimeout(() => { d.classList.add('removing'); setTimeout(() => d.remove(), 300); }, 3000);
}

export function getConfLevel(val) { 
    return val >= 90 ? 'high' : (val > 70 ? 'medium' : 'low'); 
}
