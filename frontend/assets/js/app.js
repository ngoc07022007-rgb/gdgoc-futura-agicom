import { MOCK_STRATEGIES, MOCK_CHAT_SESSIONS } from './data/mockData.js';
import { showToast } from './utils/helpers.js';
import * as Views from './views/pages.js';

let appState = {
    currentPage: 'dashboard',
    strategies: JSON.parse(JSON.stringify(MOCK_STRATEGIES)),
    activeGuidanceCmd: null,
    isScanning: false,
    aiLearned: 47
};

function init() {
    setupNav();
    setupGuidanceToolbar();
    setupModalsAndOverlays();
    renderPage('dashboard');
    setTimeout(() => { showToast('info', '👋 Chào mừng bạn quay lại, Shop PhoneMax!'); }, 800);
}

function setupNav() {
    const navItems = document.querySelectorAll('.nav-item[data-page]');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            renderPage(item.dataset.page);
        });
    });
}

function renderPage(pageId) {
    appState.currentPage = pageId;
    const container = document.getElementById('pageContent');

    const titles = {
        dashboard: { title: 'Dashboard', sub: 'Tổng quan chiến lược AI' },
        revenue: { title: 'Doanh thu & Chi phí', sub: 'Phân tích tài chính thời gian thực' },
        inventory: { title: 'Quản lý Tồn kho', sub: 'Cảnh báo và tối ưu vòng quay vốn' },
        competitor: { title: 'Phân tích Đối thủ', sub: 'So sánh giá & Market share' },
        market: { title: 'Tổng quan Thị trường', sub: 'Trending Keywords & Demand' },
        reviews: { title: 'Review Sản phẩm', sub: 'Sentiment Analysis từ khách hàng' },
        media: { title: 'Media & Quảng cáo', sub: 'Hiệu suất Ads và Content (Shopee & TikTok)' },
        chat: { title: 'Chat AI Inbox', sub: 'Hệ thống tự động phân loại và phản hồi' },
        settings: { title: 'Cài đặt & Hồ sơ', sub: 'Cấu hình Agent' }
    };

    if(titles[pageId]) {
        document.getElementById('pageTitle').textContent = titles[pageId].title;
        document.getElementById('pageSubtitle').textContent = titles[pageId].sub + ' – Cập nhật lúc ' + new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
    }

    switch (pageId) {
        case 'dashboard': container.innerHTML = Views.renderDashboardHTML(appState); break;
        case 'revenue': container.innerHTML = Views.renderRevenueHTML(); break;
        case 'inventory': container.innerHTML = Views.renderInventoryHTML(); break;
        case 'competitor': container.innerHTML = Views.renderCompetitorHTML(); break;
        case 'market': container.innerHTML = Views.renderMarketHTML(); break;
        case 'reviews': container.innerHTML = Views.renderReviewsHTML(); break;
        case 'media': container.innerHTML = Views.renderMediaHTML(); break;
        case 'settings': container.innerHTML = Views.renderSettingsHTML(); break;
        case 'chat': 
            container.innerHTML = Views.renderChatInboxHTML(); 
            const detail = document.getElementById('chatDetailContainer');
            if (detail) detail.innerHTML = Views.renderChatDetail(1);
            break;
        default: container.innerHTML = '<div class="content-card">Coming soon...</div>';
    }
}

function setupGuidanceToolbar() {
    const input = document.getElementById('guidanceInput');
    const sendBtn = document.getElementById('guidanceSendBtn');
    const tags = document.querySelectorAll('.guidance-tag');
    const activeBox = document.getElementById('guidanceActiveCmd');
    const activeTxt = document.getElementById('guidanceActiveCmdText');
    const clearBtn = document.getElementById('guidanceClearBtn');

    tags.forEach(t => t.addEventListener('click', () => input.value = t.dataset.cmd));

    function submitCmd() {
        if (!input.value.trim()) return;
        appState.activeGuidanceCmd = input.value;
        activeTxt.textContent = input.value;
        activeBox.style.display = 'flex';
        input.value = '';
        showToast('info', '🧭 Đã gửi chỉ thị chiến lược cho AI. AI đang điều chỉnh ma trận tính toán...');

        setTimeout(() => {
            if (appState.currentPage === 'dashboard') {
                let fake = {
                    id: 'strat-new-' + Date.now(), type: 'pricing', status: 'pending', confidence: 96, impact: 'high',
                    title: 'Phản hồi chỉ thị: Điều chỉnh chiến lược',
                    description: `AI đã nhận chỉ thị: "${appState.activeGuidanceCmd}". Đề xuất action phù hợp.`
                };
                appState.strategies.unshift(fake);
                renderPage('dashboard');
                showToast('success', '✨ AI đã phản hồi chỉ thị và đưa ra Strategy mới!');
            }
        }, 2500);
    }

    sendBtn.addEventListener('click', submitCmd);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') submitCmd(); });

    clearBtn.addEventListener('click', () => {
        appState.activeGuidanceCmd = null;
        activeBox.style.display = 'none';
        showToast('success', 'Đã hủy chỉ thị chiến lược. AI trở về chế độ tối ưu tự động.');
    });
}

function setupModalsAndOverlays() {
    const overlay = document.getElementById('scanOverlay');
    const btnScan = document.getElementById('btnScan');

    btnScan.addEventListener('click', () => {
        if (appState.isScanning) return;
        appState.isScanning = true;
        btnScan.classList.add('scanning');
        overlay.classList.add('show');
        
        const pb = overlay.querySelector('.scan-progress-bar');
        pb.style.animation = 'none'; pb.offsetHeight; pb.style.animation = 'scanProgress 3s forwards';

        setTimeout(() => {
            overlay.classList.remove('show');
            btnScan.classList.remove('scanning');
            appState.isScanning = false;
            showToast('success', 'Quét hoàn tất: Phát hiện luồng traffic mới.');
        }, 3000);
    });

    const modal = document.getElementById('feedbackModal');
    document.getElementById('modalCloseBtn').onclick = () => modal.classList.remove('show');
    document.getElementById('modalCancelBtn').onclick = () => modal.classList.remove('show');

    const text = document.getElementById('feedbackText');
    const sub = document.getElementById('modalSubmitBtn');
    text.oninput = () => sub.disabled = text.value.trim() === '';

    sub.onclick = () => {
        const s = appState.strategies.find(x => x.id === appState._denyTarget);
        if (s) {
            s.status = 'denied';
            s.feedback = text.value.trim();
            modal.classList.remove('show');
            text.value = '';
            showToast('error', `Đã từ chối chiến lược: ${s.title}`);
            renderPage('dashboard');
        }
    }
}

// ==========================================
// ĐĂNG KÝ HÀM GLOBAL (Dành cho các sự kiện onclick trên HTML)
// ==========================================
window.actionStrategy = function (id, action) {
    const s = appState.strategies.find(x => x.id === id);
    if (!s) return;
    if (action === 'approve') {
        s.status = 'approved';
        showToast('success', `Đã duyệt chiến lược: ${s.title}`);
        renderPage('dashboard');
    } else {
        document.getElementById('feedbackModal').classList.add('show');
        appState._denyTarget = id;
    }
}
window.approveStrategy = (id) => window.actionStrategy(id, 'approve');
window.denyStrategy = (id) => window.actionStrategy(id, 'deny');

window.selectChatConv = function (idx) {
    document.querySelectorAll('.chat-conv-item').forEach((item, i) => item.classList.toggle('active', i === idx));
    document.getElementById('chatDetailContainer').innerHTML = Views.renderChatDetail(idx);
};

window.approveChatDraft = function (idx) {
    appState.aiLearned++;
    const dNode = document.querySelector('.chat-ai-suggestion');
    if (dNode) {
        dNode.outerHTML = `<div class="chat-bubble assistant"><div class="chat-bubble-sender">Shop · Vừa xong</div>${MOCK_CHAT_SESSIONS[idx].messages[1].text}</div><div class="chat-learning-toast">📚 AI đã ghi nhớ phong cách xử lý này</div>`;
        showToast('success', 'Đã duyệt & gửi phản hồi!');
    }
};

window.editChatDraft = function (idx) {
    const tNode = document.getElementById(`draftMsg-${idx}`);
    if (tNode) {
        let oldText = tNode.textContent;
        tNode.innerHTML = `<textarea style="width:100%; min-height:60px; background:var(--bg-input); border:1px solid var(--accent-indigo); color:white; padding:8px; border-radius:4px">${oldText}</textarea>`;
        const btns = tNode.nextElementSibling.querySelectorAll('.btn-chat-action');
        btns[1].textContent = "Lưu & Gửi & Học";
        btns[1].className = "btn-chat-action btn-chat-accept";
        btns[1].onclick = () => {
            MOCK_CHAT_SESSIONS[idx].messages[1].text = tNode.querySelector('textarea').value;
            window.approveChatDraft(idx);
        };
        btns[0].style.display = 'none';
    }
};

// Khởi chạy App
document.addEventListener('DOMContentLoaded', init);
