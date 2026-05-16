// ===== ACTOR AUTOCOMPLETE =====
(function () {
    const input      = document.getElementById('actor-input');
    const dropdown   = document.getElementById('actor-dropdown');
    const hiddenId   = document.getElementById('actor-id-input');
    const hiddenName = document.getElementById('actor-name-input');
    const selectedEl = document.getElementById('selected-actor');
    const selectedNm = document.getElementById('selected-actor-name');

    if (!input) return;

    // Restore pre-selected actor name into input
    if (hiddenName && hiddenName.value) {
        input.value = hiddenName.value;
    }

    let debounceTimer;

    input.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const q = this.value.trim();

        if (q.length < 2) {
            closeDropdown();
            return;
        }

        debounceTimer = setTimeout(() => fetchActors(q), 350);
    });

    async function fetchActors(query) {
        try {
            const res  = await fetch(`/api/search-actor?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            renderDropdown(data);
        } catch (e) {
            console.error('Actor search error:', e);
        }
    }

    function renderDropdown(actors) {
        dropdown.innerHTML = '';

        if (!actors.length) {
            dropdown.innerHTML = '<div class="actor-item" style="color:#6b6b6b;cursor:default;">No results found</div>';
            dropdown.classList.add('show');
            return;
        }

        actors.forEach(actor => {
            const item = document.createElement('div');
            item.className = 'actor-item';

            const photoEl = actor.photo
                ? `<img src="${actor.photo}" alt="${actor.name}" onerror="this.style.display='none'">`
                : `<div class="actor-avatar-placeholder">🎭</div>`;

            item.innerHTML = `${photoEl}<span>${actor.name}</span>`;

            item.addEventListener('click', () => selectActor(actor));
            dropdown.appendChild(item);
        });

        dropdown.classList.add('show');
    }

    function selectActor(actor) {
        input.value      = actor.name;
        hiddenId.value   = actor.id;
        hiddenName.value = actor.name;

        // Show selected badge
        if (selectedEl && selectedNm) {
            selectedNm.textContent = actor.name;
            selectedEl.style.display = 'flex';
        }

        closeDropdown();
    }

    // Global clearActor called from HTML onclick
    window.clearActor = function () {
        input.value      = '';
        hiddenId.value   = '';
        hiddenName.value = '';
        if (selectedEl) selectedEl.style.display = 'none';
        closeDropdown();
    };

    function closeDropdown() {
        dropdown.classList.remove('show');
        dropdown.innerHTML = '';
    }

    // Close on outside click
    document.addEventListener('click', function (e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            closeDropdown();
        }
    });

    // Toggle filter panels
    window.toggleFilter = function (panelId) {
        const panel  = document.getElementById(panelId);
        const header = panel.previousElementSibling;
        if (!panel) return;
        panel.classList.toggle('open');
        header.classList.toggle('open');
    };

    // Rating slider live update
    const slider   = document.getElementById('rating-slider');
    const ratingVal = document.getElementById('rating-val');
    if (slider && ratingVal) {
        slider.addEventListener('input', function () {
            ratingVal.textContent = this.value;
        });
    }

    // Auto-open filter panels if they have active values
    const panels = ['actor-panel', 'genre-panel', 'release-panel', 'rating-panel', 'sort-panel'];
    panels.forEach(id => {
        const panel = document.getElementById(id);
        if (!panel) return;

        // Check if panel has any active inputs
        const hasActive =
            panel.querySelector('input[type="checkbox"]:checked') ||
            panel.querySelector('input[type="number"]not([value=""])') ||
            (id === 'actor-panel' && hiddenId && hiddenId.value);

        if (hasActive) {
            panel.classList.add('open');
            if (panel.previousElementSibling) {
                panel.previousElementSibling.classList.add('open');
            }
        }
    });
})();