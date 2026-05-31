function applyGlobalTheme(theme) {
    const text = document.getElementById('global-theme-text');
    const toggle = document.getElementById('theme-toggle');

    if (theme === 'light') {
        document.body.classList.add('light-theme');
        if (text) text.innerText = 'Light';
        if (toggle) {
            toggle.setAttribute('aria-pressed', 'true');
            toggle.setAttribute('aria-label', 'Ganti ke tema gelap');
        }
    } else {
        document.body.classList.remove('light-theme');
        if (text) text.innerText = 'Dark';
        if (toggle) {
            toggle.setAttribute('aria-pressed', 'false');
            toggle.setAttribute('aria-label', 'Ganti ke tema terang');
        }
    }
}

function globalToggleTheme() {
    const targetTheme = document.body.classList.contains('light-theme') ? 'dark' : 'light';
    localStorage.setItem('studio-theme', targetTheme);
    applyGlobalTheme(targetTheme);
    window.dispatchEvent(new Event('themeChanged'));
}

// Sinkronisasi tema instan
(function initTheme() {
    const savedTheme = localStorage.getItem('studio-theme') || 'dark';
    applyGlobalTheme(savedTheme);
})();

// --- Background hero toggle ---
// Ensure hero background is applied globally (no toggle UI)
function setBodyBg(enabled) {
    const bgUrl = "/static/assets/Photobooth_Background.jpeg";
    if (enabled) {
        document.body.classList.add('hero-bg');
        document.body.style.backgroundImage = `url('${bgUrl}')`;
    } else {
        document.body.classList.remove('hero-bg');
        document.body.style.backgroundImage = '';
    }
}

// apply background by default for all pages
window.addEventListener('DOMContentLoaded', function() { setBodyBg(true); });
