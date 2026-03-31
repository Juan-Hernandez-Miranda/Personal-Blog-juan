document.addEventListener("DOMContentLoaded", function () {
	// --- Carrusel de hobbies ---
	const track = document.querySelector(".hobbies-carousel-track");
	if (!track) return; // no carrusel en esta página

	const slides = Array.from(track.children);
	const total = slides.length;
	if (total <= 1) return; // nada que deslizar

	let index = 0; // índice de la imagen principal (central)

	function updateCarousel() {
		slides.forEach((slide, i) => {
			let offset = i - index;
			// Ajuste para que siempre se usen los desplazamientos más cortos (carrusel circular)
			if (offset > total / 2) offset -= total;
			if (offset < -total / 2) offset += total;

			const abs = Math.abs(offset);
			const baseX = offset * 260; // separación horizontal entre las imágenes
			const scale = 1 - Math.min(abs * 0.15, 0.55); // la central es la más grande
			const opacity = 1 - Math.min(abs * 0.25, 0.8); // laterales más transparentes
			const blur = Math.min(abs * 1.2, 4); // simula lejanía

			slide.style.transform = `translate(-50%, -50%) translateX(${baseX}px) scale(${scale})`;
			slide.style.opacity = opacity;
			slide.style.filter = `blur(${blur}px)`;
			slide.style.zIndex = String(100 - abs); // asegura que la central quede arriba
		});
	}

	updateCarousel();

	setInterval(() => {
		index = (index + 1) % total;
		updateCarousel();
	}, 4000); // cambia de imagen principal cada 4 segundos
});
