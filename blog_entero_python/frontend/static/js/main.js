document.addEventListener("DOMContentLoaded", function () {
	setupHobbiesCarousel();
	setupSearchBar();
	setupSearchResults();
	setupCreatePostForm();
});

function setupHobbiesCarousel() {
	const track = document.querySelector(".hobbies-carousel-track");
	if (!track) return;

	const slides = Array.from(track.children);
	const total = slides.length;
	if (total <= 1) return;

	let index = 0;

	function updateCarousel() {
		slides.forEach((slide, i) => {
			let offset = i - index;
			if (offset > total / 2) offset -= total;
			if (offset < -total / 2) offset += total;

			const abs = Math.abs(offset);
			const baseX = offset * 260;
			const scale = 1 - Math.min(abs * 0.15, 0.55);
			const opacity = 1 - Math.min(abs * 0.25, 0.8);
			const blur = Math.min(abs * 1.2, 4);

			slide.style.transform = `translate(-50%, -50%) translateX(${baseX}px) scale(${scale})`;
			slide.style.opacity = opacity;
			slide.style.filter = `blur(${blur}px)`;
			slide.style.zIndex = String(100 - abs);
		});
	}

	updateCarousel();

	setInterval(() => {
		index = (index + 1) % total;
		updateCarousel();
	}, 4000);
}

function setupSearchBar() {
	const searchInput = document.querySelector(".search-input");
	const searchIcon = document.querySelector(".search-icon");

	if (!searchInput || !searchIcon) return;

	const currentQuery = new URLSearchParams(window.location.search).get("q") || "";
	if (currentQuery && window.location.pathname.endsWith("search_results.html")) {
		searchInput.value = currentQuery;
	}

	const runSearch = () => {
		const query = searchInput.value.trim();
		if (!query) return;
		window.location.href = `/frontend/search_results.html?q=${encodeURIComponent(query)}`;
	};

	searchInput.addEventListener("keydown", (event) => {
		if (event.key === "Enter") {
			event.preventDefault();
			runSearch();
		}
	});

	searchIcon.addEventListener("click", runSearch);
	searchIcon.setAttribute("role", "button");
	searchIcon.setAttribute("tabindex", "0");
	searchIcon.addEventListener("keydown", (event) => {
		if (event.key === "Enter" || event.key === " ") {
			event.preventDefault();
			runSearch();
		}
	});
}

async function setupSearchResults() {
	const resultsRoot = document.querySelector("[data-search-results]");
	if (!resultsRoot) return;

	const queryInput = new URLSearchParams(window.location.search).get("q") || "";
	const queryTitle = document.querySelector("[data-search-query]");
	const statusBox = document.querySelector("[data-search-status]");

	if (queryTitle) {
		queryTitle.textContent = queryInput ? `Resultados para: ${queryInput}` : "Escribe un titulo para buscar";
	}

	if (!queryInput) {
		if (statusBox) {
			statusBox.textContent = "Escribe algo en el buscador para encontrar posts por titulo.";
		}
		return;
	}

	if (statusBox) {
		statusBox.textContent = "Buscando posts...";
	}

	try {
		const response = await fetch(`/posts/search?q=${encodeURIComponent(queryInput)}`);
		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}

		const posts = await response.json();
		resultsRoot.innerHTML = "";

		if (!posts.length) {
			if (statusBox) {
				statusBox.textContent = "No se encontraron posts con ese titulo.";
			}
			resultsRoot.innerHTML = '<p class="search-empty">No hay resultados. Prueba con otra palabra.</p>';
			return;
		}

		if (statusBox) {
			statusBox.textContent = `Se encontraron ${posts.length} post(s).`;
		}

		posts.forEach((post) => {
			const article = document.createElement("article");
			article.className = "search-result-card";

			const image = post.imagen_url
				? `<img src="${post.imagen_url}" alt="${escapeHtml(post.titulo)}">`
				: `<div class="search-result-placeholder">Sin imagen</div>`;

			article.innerHTML = `
				${image}
				<div class="search-result-content">
					<p class="search-result-meta">Post #${post.id} | ${formatDate(post.fecha_creacion)}</p>
					<h3>${escapeHtml(post.titulo)}</h3>
					<p>${escapeHtml(post.descripcion || post.contenido.slice(0, 180))}</p>
				</div>
			`;

			resultsRoot.appendChild(article);
		});
	} catch (error) {
		console.error("Error buscando posts:", error);
		if (statusBox) {
			statusBox.textContent = "No se pudo completar la busqueda.";
		}
		resultsRoot.innerHTML = '<p class="search-empty">Hubo un error consultando la busqueda.</p>';
	}
}

function setupCreatePostForm() {
	const form = document.querySelector("[data-create-post-form]");
	if (!form) return;

	const categorySelect = form.querySelector("[data-category-select]");
	const submitButton = form.querySelector('button[type="submit"]');
	const statusBox = form.querySelector("[data-form-status]");

	const setStatus = (message, type = "info") => {
		if (!statusBox) return;
		statusBox.textContent = message;
		statusBox.dataset.statusType = type;
	};

	const loadCategories = async () => {
		if (!categorySelect) return;

		try {
			const response = await fetch("/categorias/");
			if (!response.ok) {
				throw new Error(`HTTP ${response.status}`);
			}

			const categories = await response.json();
			categorySelect.innerHTML = '<option value="">Selecciona una categoria</option>';

			if (!categories.length) {
				categorySelect.innerHTML = '<option value="">No hay categorias creadas</option>';
				if (submitButton) submitButton.disabled = true;
				setStatus("Primero crea una categoria para poder guardar posts.", "error");
				return;
			}

			categories.forEach((category) => {
				const option = document.createElement("option");
				option.value = String(category.id);
				option.textContent = category.nombre;
				categorySelect.appendChild(option);
			});
		} catch (error) {
			console.error("Error cargando categorias:", error);
			if (submitButton) submitButton.disabled = true;
			setStatus("No se pudieron cargar las categorias.", "error");
		}
	};

	form.addEventListener("submit", async (event) => {
		event.preventDefault();

		const formData = new FormData(form);
		const payload = {
			titulo: String(formData.get("titulo") || "").trim(),
			descripcion: String(formData.get("descripcion") || "").trim() || null,
			contenido: String(formData.get("contenido") || "").trim(),
			categoria_id: Number(formData.get("categoria_id")),
			imagen_url: String(formData.get("imagen_url") || "").trim() || null,
		};

		if (!payload.titulo || !payload.contenido || !payload.categoria_id) {
			setStatus("Titulo, contenido y categoria son obligatorios.", "error");
			return;
		}

		if (submitButton) submitButton.disabled = true;
		setStatus("Guardando post...", "info");

		try {
			const response = await fetch("/posts/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				throw new Error(errorData.detail || `HTTP ${response.status}`);
			}

			const createdPost = await response.json();
			setStatus(`Post creado: ${createdPost.titulo}. Redirigiendo...`, "success");
			form.reset();

			setTimeout(() => {
				window.location.href = `/frontend/search_results.html?q=${encodeURIComponent(createdPost.titulo)}`;
			}, 900);
		} catch (error) {
			console.error("Error creando post:", error);
			setStatus(`No se pudo crear el post: ${error.message}`, "error");
		} finally {
			if (submitButton) submitButton.disabled = false;
		}
	});

	loadCategories();
}

function escapeHtml(value) {
	return String(value)
		.replaceAll("&", "&amp;")
		.replaceAll("<", "&lt;")
		.replaceAll(">", "&gt;")
		.replaceAll('"', "&quot;")
		.replaceAll("'", "&#39;");
}

function formatDate(value) {
	if (!value) return "";
	const date = new Date(value);
	if (Number.isNaN(date.getTime())) return "";
	return date.toLocaleDateString("es-MX", {
		year: "numeric",
		month: "short",
		day: "numeric",
	});
}
