// ===================================================================
// AI College Placement Management System - Main JavaScript Logic
// ===================================================================

document.addEventListener('DOMContentLoaded', () => {
    initThemeSwitcher();
    initNavbar();
    initAlerts();
    initQuickTooltips();
});

// Mobile Navbar & Dropdown Handlers
function initNavbar() {
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('active');
        });
    }

    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
            if (navLinks && !navLinks.contains(e.target) && !mobileToggle.contains(e.target)) {
                navLinks.classList.remove('active');
            }
        });
    }
}

// Auto dismiss alerts after 5 seconds
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => alert.remove());
        }
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(20px)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(() => alert.remove(), 400);
        }, 6000);
    });
}

function initQuickTooltips() {
    // Optional tooltip enhancement
}

// CSRF Token Helper for AJAX calls in Django
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    if (cookieValue) return cookieValue;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
}

// AI Chat Interaction Engine
window.AIChatEngine = {
    init: function(chatMessagesId, inputId, sendBtnId, apiEndpoint) {
        const chatMessages = document.getElementById(chatMessagesId);
        const chatInput = document.getElementById(inputId);
        const sendBtn = document.getElementById(sendBtnId);

        if (!chatMessages || !chatInput || !sendBtn) return;

        const scrollToBottom = () => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        const appendMessage = (sender, text, isMarkdown = false) => {
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-message ${sender}`;
            
            const avatar = document.createElement('div');
            avatar.className = sender === 'user' ? 'avatar-circle' : 'ai-bot-avatar';
            avatar.style.width = '36px';
            avatar.style.height = '36px';
            avatar.style.fontSize = '0.9rem';
            avatar.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-brain"></i>';

            const bubble = document.createElement('div');
            bubble.className = 'chat-bubble';
            bubble.innerHTML = isMarkdown ? text : escapeHtml(text).replace(/\n/g, '<br>');

            msgDiv.appendChild(avatar);
            msgDiv.appendChild(bubble);
            chatMessages.appendChild(msgDiv);
            scrollToBottom();
            return bubble;
        };

        const showTypingIndicator = () => {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'chat-message ai typing-indicator-msg';
            typingDiv.id = 'aiTypingIndicator';
            typingDiv.innerHTML = `
                <div class="ai-bot-avatar" style="width: 36px; height: 36px; font-size: 0.9rem;">
                    <i class="fa-solid fa-brain"></i>
                </div>
                <div class="chat-bubble" style="color: #64748b; font-style: italic;">
                    <i class="fa-solid fa-spinner fa-spin"></i> AI is thinking and preparing recommendations...
                </div>
            `;
            chatMessages.appendChild(typingDiv);
            scrollToBottom();
        };

        const removeTypingIndicator = () => {
            const indicator = document.getElementById('aiTypingIndicator');
            if (indicator) indicator.remove();
        };

        const sendMessage = async (textToSend) => {
            const message = (textToSend || chatInput.value).trim();
            if (!message) return;

            appendMessage('user', message);
            chatInput.value = '';
            showTypingIndicator();

            try {
                const response = await fetch(apiEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: JSON.stringify({ message: message })
                });

                removeTypingIndicator();

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                appendMessage('ai', data.reply, true);
            } catch (err) {
                removeTypingIndicator();
                appendMessage('ai', "I'm currently unable to connect to the AI engine, but you can explore current placement drives, browse eligibility criteria, or try asking about specific roles like Python Developer, Data Analyst, or Cloud Engineer!");
            }
        };

        sendBtn.addEventListener('click', () => sendMessage());
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Quick prompt buttons support
        document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const prompt = btn.getAttribute('data-prompt') || btn.innerText.trim();
                sendMessage(prompt);
            });
        });
    }
};

function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Modern Dark / Light Theme Switcher
function initThemeSwitcher() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', nextTheme);
            localStorage.setItem('theme', nextTheme);
            updateThemeIcon(nextTheme);
        });
    }
}

function updateThemeIcon(theme) {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (!toggleBtn) return;
    const icon = toggleBtn.querySelector('i');
    if (!icon) return;

    if (theme === 'dark') {
        icon.className = 'fa-solid fa-sun';
        icon.style.color = '#f59e0b';
        toggleBtn.setAttribute('title', 'Switch to Light Mode');
    } else {
        icon.className = 'fa-solid fa-moon';
        icon.style.color = '#6366f1';
        toggleBtn.setAttribute('title', 'Switch to Dark Mode');
    }
}

