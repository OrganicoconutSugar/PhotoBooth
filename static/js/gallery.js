function updateFrameNumbers() {
    const frameLabels = document.querySelectorAll('.frame-number');
    frameLabels.forEach((label, index) => {
        label.innerText = `Foto ${index + 1}`;
    });

    const remainingCards = document.querySelectorAll('.gallery-card');
    if (remainingCards.length === 0) {
        const grid = document.getElementById('gallery-grid');
        const dynamicEmpty = document.getElementById('dynamic-empty-state');
        const emptyState = document.getElementById('empty-state');
        if (grid) grid.classList.add('hidden');
        if (dynamicEmpty) dynamicEmpty.classList.remove('hidden');
        if (emptyState) emptyState.classList.remove('hidden');
    }
}

function removeCardElement(buttonElement) {
    const card = buttonElement.closest('.gallery-card');
    if (card) {
        gsap.to(card, {
            opacity: 0,
            scale: 0.8,
            y: 15,
            duration: 0.3,
            onComplete: () => {
                card.remove();
                updateFrameNumbers();
            }
        });
    }
}

function deletePhoto(filename, buttonElement) {
    if (confirm('Hapus foto ini secara permanen?')) {
        fetch(`/delete-photo/${filename}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (response.ok || response.status === 404) {
                    removeCardElement(buttonElement);
                } else {
                    removeCardElement(buttonElement);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                removeCardElement(buttonElement);
            });
    }
}

window.addEventListener('DOMContentLoaded', () => {
    updateFrameNumbers();
    gsap.from('.gallery-title', { opacity: 0, y: 20, duration: 0.8, ease: "power3.out" });
    gsap.from('.gallery-card', {
        y: 25,
        duration: 0.8,
        stagger: 0.08,
        ease: "power3.out"
    });
});
