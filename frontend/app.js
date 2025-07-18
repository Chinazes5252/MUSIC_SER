// app.js
class MusicPlayer {
    constructor() {
        // Инициализация пользователя и токена
        this.userId = Telegram.WebApp.initDataUnsafe.user.id;
        this.token = window.PUBLIC_TOKEN;
        this.player = new Audio();

        // Telegram Web App
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();

        this.initEventListeners();
    }

    async request(path, options = {}) {
        // Добавляем заголовок авторизации
        options.headers = {
            ...options.headers,
            'X-Token': this.token,
            'X-Telegram-Init-Data': Telegram.WebApp.initData
        };

        const response = await fetch(`${API_BASE_URL}${path}`, options);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response;
    }

    async search() {
        const query = document.getElementById('search-input').value.trim();
        if (!query) return;

        this.showLoader();
        try {
            const res = await this.request(`/api/search?q=${encodeURIComponent(query)}`);
            const items = await res.json();
            this.displayResults(items);
        } catch (e) {
            this.showError(`Ошибка поиска: ${e.message}`);
        } finally {
            this.hideLoader();
        }
    }

    async playTrack(videoId) {
        try {
            const res = await this.request(`/api/stream?id=${videoId}`);
            const url = await res.text();
            this.player.src = url;
            await this.player.play();
        } catch (e) {
            this.showError(`Ошибка воспроизведения: ${e.message}`);
        }
    }

    async saveTrack(videoId) {
        try {
            const res = await this.request('/api/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user_id: this.userId, track_id: videoId })
            });
            const result = await res.json();
            if (result.status === 'saved') {
                Telegram.WebApp.showAlert('✅ Трек сохранён!');
            } else if (result.status === 'already_exists') {
                Telegram.WebApp.showAlert('⚠️ Уже в библиотеке');
            }
        } catch (e) {
            this.showError(`Ошибка сохранения: ${e.message}`);
        }
    }

    displayResults(items) {
        const container = document.getElementById('results');
        container.innerHTML = items.map(item => `
            <div class="track-card" data-id="${item.id}">
                <img src="${item.thumbnail}"/>
                <div class="track-info">
                    <h3>${item.title}</h3>
                    <p>${item.channel}</p>
                    <button class="play-btn">▶ Play</button>
                    <button class="save-btn">💾 Save</button>
                </div>
            </div>
        `).join('');
    }

    initEventListeners() {
        document.getElementById('search-btn').addEventListener('click', () => this.search());
        document.getElementById('search-input').addEventListener('keypress', e => {
            if (e.key === 'Enter') this.search();
        });

        document.getElementById('results').addEventListener('click', e => {
            const card = e.target.closest('.track-card');
            if (!card) return;
            const videoId = card.dataset.id;
            if (e.target.classList.contains('play-btn')) {
                this.playTrack(videoId);
            } else if (e.target.classList.contains('save-btn')) {
                this.saveTrack(videoId);
            }
        });
    }

    showLoader() {
        document.body.classList.add('loading');
    }

    hideLoader() {
        document.body.classList.remove('loading');
    }

    showError(message) {
        Telegram.WebApp.showAlert(message);
    }
}

// Инициализация
window.player = new MusicPlayer();