// ===================== КОНФИГУРАЦИЯ API =====================###
// Определяем рабочий backend URL (поддержка localhost и file:// режима)
let API_BASE_URL = '';

async function detectApiBaseUrl() {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    const isLocal = protocol === 'file:' || !hostname || hostname === 'localhost' || hostname === '127.0.0.1';

    const candidates = isLocal
        ? [
            'http://localhost:8000',
            'http://127.0.0.1:8000',
            'http://localhost:8888',
            'http://127.0.0.1:8888'
        ]
        : [`${protocol}//${hostname}`];

    for (const baseUrl of candidates) {
        try {
            const response = await fetch(`${baseUrl}/stats`);
            if (response.ok) return baseUrl;
        } catch (_) {
            // Игнорируем сетевые ошибки и пробуем следующий URL
        }
    }

    // Fallback: используем первый кандидат, чтобы ошибки были явными в UI/console
    return candidates[0];
}

// ===================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====================
let currentUserId = null;
let currentChatUserId = null;
let allUsers = [];
let chatMessages = [];

// ===================== ИНИЦИАЛИЗАЦИЯ =====================
document.addEventListener('DOMContentLoaded', async () => {
    API_BASE_URL = await detectApiBaseUrl();
    console.log('API base URL:', API_BASE_URL);

    loadUsers();
    loadStats();
    // Обновление статистики каждые 5 секунд
    setInterval(loadStats, 5000);
});

// ===================== ЗАГРУЗКА ПОЛЬЗОВАТЕЛЕЙ =====================
async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        if (!response.ok) throw new Error('Ошибка загрузки пользователей');
        
        allUsers = await response.json();
        displayUsers(allUsers);
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('usersList').innerHTML = '<li class="loading">Ошибка загрузки</li>';
    }
}

// ===================== ОТОБРАЖЕНИЕ ПОЛЬЗОВАТЕЛЕЙ =====================
function displayUsers(users) {
    const usersList = document.getElementById('usersList');
    
    if (users.length === 0) {
        usersList.innerHTML = '<li class="loading">Нет пользователей</li>';
        return;
    }
    
    usersList.innerHTML = users.map(user => `
        <li onclick="selectUser(${user.id}, '${user.username}')" 
            class="${currentChatUserId === user.id ? 'active' : ''}">
            👤 ${user.username}
        </li>
    `).join('');
}

// ===================== ПОИСК ПОЛЬЗОВАТЕЛЕЙ =====================
async function searchUsers() {
    const searchInput = document.getElementById('searchInput').value.trim();
    
    if (!searchInput) {
        displayUsers(allUsers);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/search/${encodeURIComponent(searchInput)}`);
        if (!response.ok) throw new Error('Ошибка поиска');
        
        const results = await response.json();
        displayUsers(results);
    } catch (error) {
        console.error('Ошибка поиска:', error);
        displayUsers([]);
    }
}

// ===================== СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ =====================
async function createUser() {
    const username = document.getElementById('newUsername').value.trim();
    const email = document.getElementById('newEmail').value.trim();
    
    if (!username || !email) {
        alert('Пожалуйста, заполните все поля');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email })
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert('Ошибка: ' + (error.detail || 'Не удалось создать пользователя'));
            return;
        }
        
        const newUser = await response.json();
        currentUserId = newUser.id;
        
        // Очистка формы
        document.getElementById('newUsername').value = '';
        document.getElementById('newEmail').value = '';
        
        alert('✅ Пользователь успешно создан!');
        loadUsers();
        loadStats();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при создании пользователя');
    }
}

// ===================== ВЫБОР ПОЛЬЗОВАТЕЛЯ ДЛЯ ЧАТА =====================
async function selectUser(userId, username) {
    if (!currentUserId) {
        alert('❌ Сначала создайте свой пользователь слева');
        return;
    }
    
    if (userId === currentUserId) {
        alert('❌ Вы не можете отправить сообщение самому себе');
        return;
    }
    
    currentChatUserId = userId;
    
    // Обновление активного пользователя в списке
    document.querySelectorAll('.list li').forEach(li => {
        if (parseInt(li.textContent.match(/\d+/)) === userId || li.innerHTML.includes(`selectUser(${userId}`)) {
            li.classList.add('active');
        } else {
            li.classList.remove('active');
        }
    });
    
    // Обновление заголовка чата
    document.getElementById('chatHeaderContent').innerHTML = `
        <h2>💬 ${escapeHtml(username)}</h2>
        <p>Открыт чат с: <strong>${escapeHtml(username)}</strong></p>
    `;
    
    // Показать форму ввода
    document.getElementById('messageForm').style.display = 'flex';
    
    // Загрузить историю чата
    loadConversation(currentUserId, userId);
}

// ===================== ЗАГРУЗКА ИСТОРИИ ЧАТА =====================
async function loadConversation(user1Id, user2Id) {
    try {
        const response = await fetch(`${API_BASE_URL}/messages/conversation/${user1Id}/${user2Id}`);
        if (!response.ok) throw new Error('Ошибка загрузки');
        
        chatMessages = await response.json();
        displayMessages();
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('messagesContainer').innerHTML = 
            '<div class="welcome-message"><p>Ошибка загрузки чата</p></div>';
    }
}

// ===================== ОТПРАВКА СООБЩЕНИЯ =====================
async function sendMessage() {
    const messageText = document.getElementById('messageInput').value.trim();
    
    if (!messageText) {
        alert('Напишите сообщение');
        return;
    }
    
    if (!currentUserId || !currentChatUserId) {
        alert('Ошибка: выберите пользователя');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sender_id: currentUserId,
                receiver_id: currentChatUserId,
                content: messageText
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert('Ошибка: ' + (error.detail || 'Не удалось отправить'));
            return;
        }
        
        // Очистка поля ввода
        document.getElementById('messageInput').value = '';
        
        // Перезагрузка чата
        loadConversation(currentUserId, currentChatUserId);
        loadStats();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при отправке сообщения');
    }
}

// ===================== ОТОБРАЖЕНИЕ СООБЩЕНИЙ =====================
function displayMessages() {
    const container = document.getElementById('messagesContainer');
    
    if (chatMessages.length === 0) {
        container.innerHTML = `
            <div class="welcome-message">
                <p>💬 Нет сообщений</p>
                <p>Напишите первое сообщение!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = chatMessages.map(msg => {
        const isFromMe = msg.sender_id === currentUserId;
        const date = new Date(msg.created_at);
        const timeStr = date.toLocaleTimeString('ru-RU', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        return `
            <div class="message ${isFromMe ? 'message-receiver' : 'message-sender'}">
                <div class="message-content">
                    <span>${escapeHtml(msg.content)}</span>
                    <div class="message-timestamp">${timeStr}</div>
                </div>
            </div>
        `;
    }).join('');
    
    // Прокрутка вниз
    setTimeout(() => {
        container.scrollTop = container.scrollHeight;
    }, 100);
}

// ===================== ОЧИСТКА ЧАТА =====================
function clearChat() {
    if (confirm('Вы уверены? История не будет удалена из базы данных.')) {
        document.getElementById('messagesContainer').innerHTML = '';
        document.getElementById('messageInput').value = '';
    }
}

// ===================== ЗАГРУЗКА СТАТИСТИКИ =====================
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (!response.ok) throw new Error('Ошибка');
        
        const stats = await response.json();
        document.getElementById('usersCount').textContent = stats.users_count;
        document.getElementById('messagesCount').textContent = stats.messages_count;
    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
    }
}

// ===================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===================== EMOJI PICKER =====================
function toggleEmojiPicker() {
    const emojiPicker = document.getElementById('emojiPicker');
    const emojiBtn = document.querySelector('.emoji-picker-btn');
    
    if (emojiPicker.classList.contains('show')) {
        emojiPicker.classList.remove('show');
    } else {
        // Позиционируем picker над кнопкой
        const rect = emojiBtn.getBoundingClientRect();
        emojiPicker.style.bottom = (window.innerHeight - rect.top + 10) + 'px';
        emojiPicker.style.left = rect.left + 'px';
        emojiPicker.classList.add('show');
    }
}

function addEmoji(emoji) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value += emoji;
    messageInput.focus();
    // Закрыть picker после выбора
    document.getElementById('emojiPicker').classList.remove('show');
}

// Закрыть emoji picker при клике вне его
document.addEventListener('click', (e) => {
    const emojiPicker = document.getElementById('emojiPicker');
    const emojiBtn = document.querySelector('.emoji-picker-btn');
    if (emojiPicker && !emojiPicker.contains(e.target) && emojiBtn && !emojiBtn.contains(e.target)) {
        emojiPicker.classList.remove('show');
    }
});

// Закрыть emoji picker при клике вне его
document.addEventListener('click', (e) => {
    const emojiPicker = document.getElementById('emojiPicker');
    const emojiBtn = document.querySelector('.emoji-picker-btn');
    if (!emojiPicker.contains(e.target) && !emojiBtn.contains(e.target)) {
        emojiPicker.classList.remove('show');
    }
});

// ===================== ПОДДЕРЖКА ENTER ДЛЯ ОТПРАВКИ =====================
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        sendMessage();
    }
});
