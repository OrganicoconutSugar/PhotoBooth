window.addEventListener('DOMContentLoaded', () => {
    gsap.from('.profile-card', {
        opacity: 0,
        y: 30,
        scale: 0.95,
        duration: 0.8,
        ease: "power3.out"
    });
});
