import { MOCK_CHAT_SESSIONS } from '../data/mockData.js';

export function renderDashboardHTML(appState) {
    return `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
      <div class="filter-tabs" style="border-bottom:none">
        <button class="filter-tab active" style="margin-left:0">Tất cả sàn</button>
        <button class="filter-tab">Shopee</button>
        <button class="filter-tab">Tiki</button>
        <button class="filter-tab">Website</button>
      </div>
      <div class="filter-tabs" style="border-bottom:none">
        <button class="filter-tab">Hôm nay</button>
        <button class="filter-tab active">7 Ngày qua</button>
        <button class="filter-tab">30 Ngày qua</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card indigo">
        <div class="stat-card-header" style="display:flex; justify-content:space-between; align-items:flex-start">
          <div class="stat-card-label">Doanh thu</div>
          <div style="background:var(--accent-indigo-bg); color:var(--accent-indigo); width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:1.1rem">💰</div>
        </div>
        <div class="stat-card-value" style="font-size:1.8rem; margin:8px 0; font-weight:800; line-height:1">120.5<span style="font-size:1rem; color:var(--text-muted)">M₫</span></div>
        <div class="stat-card-trend up" style="font-size:0.8rem; font-weight:600">↑ 15% vs kỳ trước</div>
      </div>
      
      <div class="stat-card emerald">
        <div class="stat-card-header" style="display:flex; justify-content:space-between; align-items:flex-start">
          <div class="stat-card-label">Tổng Đơn Hàng</div>
          <div style="background:var(--accent-emerald-bg); color:var(--accent-emerald); width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:1.1rem">📦</div>
        </div>
        <div class="stat-card-value" style="font-size:1.8rem; margin:8px 0; font-weight:800; line-height:1">450</div>
        <div class="stat-card-trend up" style="font-size:0.8rem; font-weight:600">↑ 5% vs kỳ trước</div>
      </div>
      
      <div class="stat-card rose">
        <div class="stat-card-header" style="display:flex; justify-content:space-between; align-items:flex-start">
          <div class="stat-card-label">Tỷ Lệ Chuyển Đổi (CR)</div>
          <div style="background:var(--accent-rose-bg); color:var(--accent-rose); width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:1.1rem">🎯</div>
        </div>
        <div class="stat-card-value" style="font-size:1.8rem; margin:8px 0; font-weight:800; line-height:1">3.2<span style="font-size:1rem; color:var(--text-muted)">%</span></div>
        <div class="stat-card-trend down" style="font-size:0.8rem; font-weight:600">↓ 0.5% vs kỳ trước</div>
      </div>
      
      <div class="stat-card amber">
        <div class="stat-card-header" style="display:flex; justify-content:space-between; align-items:flex-start">
          <div class="stat-card-label">AOV (Giỏ hàng)</div>
          <div style="background:var(--accent-amber-bg); color:var(--accent-amber); width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:1.1rem">🛒</div>
        </div>
        <div class="stat-card-value" style="font-size:1.8rem; margin:8px 0; font-weight:800; line-height:1">266<span style="font-size:1rem; color:var(--text-muted)">K</span></div>
        <div class="stat-card-trend up" style="font-size:0.8rem; font-weight:600">↑ 2% vs kỳ trước</div>
      </div>
    </div>

    <div class="content-card" style="border-left: 4px solid var(--accent-indigo); background: rgba(234, 179, 8, 0.05); margin-top: 24px;">
      <div style="display:flex; gap:12px; align-items:flex-start;">
        <div style="font-size:2.5rem; line-height:1">💡</div>
        <div>
          <h4 style="font-size:1rem; font-weight:700; color:var(--text-heading); margin-bottom:8px;">AgiCom Insight (Phân tích chuyên sâu)</h4>
          <p style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6; margin:0">
            Doanh thu đang tập trung mạnh vào sàn <b>Shopee (65%)</b> với sản phẩm chủ lực là "Tai nghe Bluetooth". 
            Tuy nhiên, tỷ lệ chuyển đổi (CR) đang có dấu hiệu giảm nhẹ.<br/>
            👉 <b>Đề xuất chiến lược:</b> Tăng 15% ngân sách quảng cáo nội sàn Shopee cho Top 3 SKU. Set thêm Flash Sale khung giờ vàng cuối tuần này để kéo lại CR.
          </p>
        </div>
      </div>
    </div>

    <div class="dashboard-grid" style="margin-top:24px">
      <div class="strategy-list">
        <div class="section-header">
          <div><h2 class="section-title">Danh sách Khuyến nghị / Chiến lược</h2><p class="section-subtitle">Đề xuất tự động từ AI Agent</p></div>
        </div>
        ${appState.strategies.map(s => renderStrategyCardHTML(s)).join('')}
      </div>
    </div>
  `;
}

export function renderStrategyCardHTML(s) {
  let typeBadge = '';
  if(s.type === 'pricing') typeBadge = '<div class="badge-type pricing">💰 CẠNH TRANH GIÁ</div>';
  else if(s.type === 'content') typeBadge = '<div class="badge-type content">📝 TỐI ƯU NỘI DUNG</div>';
  else typeBadge = '<div class="badge-type chat_response">💬 XỬ LÝ KHIẾU NẠI</div>';
  
  let statusBadge = '';
  if(s.status === 'pending') statusBadge = '<div class="badge-status pending">● Chờ duyệt</div>';
  else if(s.status === 'approved') statusBadge = '<div class="badge-status approved">● Tự động Duyệt</div>';
  else statusBadge = '<div class="badge-status denied">● Đã từ chối</div>';
  
  let currentVal = "250.000đ";
  let suggestVal = "250.000đ";
  let reasonText = "Duy trì mức giá hiện tại là 250.000đ dựa trên chiến lược định giá Premium.";
  let contentText = "Cần cập nhật ngay thông tin về tính năng vào tiêu đề.";
  
  if (s.id === 'strat-001') { currentVal = "28.500.000đ"; suggestVal = "27.790.000đ"; }
  else if (s.id === 'strat-002') { currentVal = "5.450.000đ"; suggestVal = "5.690.000đ"; }
  
  return `
    <div class="strategy-card" id="stratCard-${s.id}">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
        ${typeBadge}
        ${statusBadge}
      </div>
      
      <h2 class="strategy-title">Đề xuất: ${s.type === 'pricing' ? suggestVal : s.title}</h2>
      
      <div class="strategy-description">
        <p><b>Lý do:</b> ${s.description || reasonText}</p>
        <p><b>Nội dung:</b> ${contentText}</p>
      </div>
      
      ${s.type === 'pricing' ? `
      <div class="comparison-box-container">
        <div class="comp-col">
          <div class="comp-label">HIỆN TẠI</div>
          <div class="comp-val">${currentVal}</div>
        </div>
        <div class="comp-arrow">➔</div>
        <div class="comp-col">
          <div class="comp-label">ĐỀ XUẤT (AI)</div>
          <div class="comp-val suggest">${suggestVal}</div>
        </div>
      </div>` : ''}
      
      <div class="confidence-row">
        <span class="conf-label">Độ tin cậy AI:</span>
        <div class="conf-progress"><div class="conf-fill" style="width: ${s.confidence}%"></div></div>
        <span class="conf-value">${s.confidence}%</span>
      </div>
      
      <div class="reasoning-toggle" onclick="this.nextElementSibling.classList.toggle('open')">
        🔍 Giải thích Lý do (AI) ▲
      </div>
      <div class="reasoning-content open">
        <p><b style="color: #ca8a04">✨ Thực thi chiến lược do Giám đốc ủy quyền:</b> Hệ thống phát hiện biến động chỉ số dựa trên dữ liệu mua sắm theo yêu cầu của bạn.</p>
      </div>
      
      ${s.status === 'pending' ? `
      <div class="action-buttons">
        <button class="btn-approve" onclick="window.approveStrategy('${s.id}')">✅ Duyệt ngay</button>
        <button class="btn-reject" onclick="window.denyStrategy('${s.id}')">❌ Bỏ qua</button>
      </div>
      ` : ''}
    </div>
  `;
}

export function renderRevenueHTML() {
    return `
    <div class="grid-2">
      <div class="content-card">
        <h3 class="content-card-title">Doanh Thu 7 Ngày Qua</h3>
        <div class="bar-chart" style="height: 250px">
          ${[4, 6, 5, 8, 7, 10, 9].map((v, i) => `
            <div class="bar-col">
              <div class="bar-value">${v}0M</div>
              <div class="bar-fill" style="height: ${v * 10}%"></div>
              <div class="bar-label">T${i + 2}</div>
            </div>
          `).join('')}
        </div>
      </div>
      
      <div class="content-card">
        <h3 class="content-card-title">Báo Cáo Lợi Nhuận (P&L)</h3>
        <table class="data-table">
          <thead><tr><th>Hạng mục</th><th>Giá trị</th><th>Trend</th></tr></thead>
          <tbody>
            <tr><td>1. Doanh thu gộp</td><td>850,000,000₫</td><td class="value-positive">↑ 5%</td></tr>
            <tr><td>2. Giá vốn (COGS)</td><td>610,000,000₫</td><td>-</td></tr>
            <tr><td>3. Phí Sàn</td><td>59,500,000₫</td><td class="value-negative">~7%</td></tr>
            <tr><td>4. Phí Quảng Cáo</td><td>42,000,000₫</td><td>~5%</td></tr>
            <tr style="border-top: 2px solid var(--border-primary)">
              <td style="font-weight: 700;">LỢI NHUẬN RÒNG</td>
              <td style="font-weight: 800; color: var(--accent-emerald)">130,000,000₫</td>
              <td class="value-positive">Marg 15.3%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

export function renderInventoryHTML() {
    return `
    <div class="stats-grid" style="margin-bottom: -10px">
      <div class="stat-card"><div class="stat-card-label">Tổng Kho</div><div class="stat-card-value">2,450</div></div>
      <div class="stat-card amber"><div class="stat-card-label">Sắp Hết Cần Nhập</div><div class="stat-card-value">5 SKU</div></div>
      <div class="stat-card rose"><div class="stat-card-label">Tồn Lâu (Khó bán)</div><div class="stat-card-value">12 SKU</div></div>
    </div>
    
    <div class="grid-2" style="margin-top: 24px;">
      <div class="content-card">
        <h3 class="content-card-title">Cảnh Báo Sắp Hết Hàng</h3>
        <table class="data-table">
          <thead><tr><th>Sản Phẩm</th><th>Số Lượng</th><th>Turnover</th></tr></thead>
          <tbody>
            <tr><td>S24 Ultra Case Spigen</td><td class="value-negative">2</td><td>3 ngày</td></tr>
            <tr><td>Cáp Anker 100W</td><td class="value-negative">5</td><td>4 ngày</td></tr>
          </tbody>
        </table>
      </div>
      <div class="content-card">
        <h3 class="content-card-title">Cảnh Báo Tồn Lâu (Cần Đẩy)</h3>
        <table class="data-table">
          <thead><tr><th>Sản Phẩm</th><th>Kho</th><th>Ngày Tồn</th></tr></thead>
          <tbody>
            <tr><td>Mi Band 7 Xanh</td><td>45</td><td class="value-negative">80 ngày</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

export function renderCompetitorHTML() {
    return `
    <div class="grid-2">
      <div class="content-card">
        <h3 class="content-card-title">Biến Động Giá - Đối Thủ</h3>
        <table class="data-table">
          <thead><tr><th>Shop</th><th>Giá Cũ</th><th>Giá Mới</th><th>Trend</th></tr></thead>
          <tbody>
            <tr><td><span class="table-badge green">Shop Của Bạn</span></td><td>-</td><td>29,990,000₫</td><td>-</td></tr>
            <tr><td>Hoàng Hà</td><td>30,490,000₫</td><td>28,490,000₫</td><td class="value-negative">↓ 6.5%</td></tr>
            <tr><td>CellphoneS</td><td>28,990,000₫</td><td>28,990,000₫</td><td>-</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

export function renderMarketHTML() {
    return `
    <div class="content-card">
      <h3 class="content-card-title">Từ Khóa Tìm Kiếm Trending</h3>
      <div class="tag-cloud">
        <span class="tag-item hot">Sạc dự phòng không dây mini</span>
        <span class="tag-item hot">iPhone 15 pro max cũ 99%</span>
        <span class="tag-item trending">Loa marshall stanmore 3</span>
      </div>
    </div>
  `;
}

export function renderReviewsHTML() {
    return `
    <div class="grid-2">
      <div class="review-card">
        <div class="review-card-header"><span class="review-card-author">khachhang_vip</span><span class="review-card-date">Hôm qua</span></div>
        <div class="star-display"><span class="star filled">★</span><span class="star filled">★</span><span class="star empty">★</span><span class="star empty">★</span><span class="star empty">★</span></div>
        <div class="review-card-text">Giao hàng hộp bị móp nặng. Mong shop nhắc bên vận chuyển cẩn thận hơn.</div>
        <div class="review-card-sentiment negative">Vấn đề: Đóng gói</div>
      </div>
      <div class="review-card">
        <div class="review-card-header"><span class="review-card-author">nguyentuan123</span><span class="review-card-date">2 ngày trước</span></div>
        <div class="star-display"><span class="star filled">★</span><span class="star filled">★</span><span class="star filled">★</span><span class="star filled">★</span><span class="star filled">★</span></div>
        <div class="review-card-text">Máy móc thì ngon lành, bot tư vấn nhiệt tình. 10 điểm.</div>
        <div class="review-card-sentiment positive">Điểm khen: AI Chat Support</div>
      </div>
    </div>
  `;
}

export function renderMediaHTML() {
    return `
    <div class="content-card">
      <h3 class="content-card-title">Hiệu Suất Quảng Cáo</h3>
      <table class="data-table">
        <thead><tr><th>Campaign (Mã hàng)</th><th>Chi phí</th><th>Chuyển Đổi</th><th>ROAS</th><th>AI Action</th></tr></thead>
        <tbody>
          <tr><td>Tai nghe AirPods Pro 2</td><td>4,000,000₫</td><td>45 đơn</td><td class="value-positive">12.5x</td><td><span class="table-badge green">Tự Build Scale</span></td></tr>
          <tr><td>Ốp Silicon chống bẩn</td><td>1,700,000₫</td><td>8 đơn</td><td class="value-negative">0.8x</td><td><span class="table-badge red">Tự Cắt giảm</span></td></tr>
        </tbody>
      </table>
    </div>
  `;
}

export function renderChatInboxHTML() {
    return `
    <div class="chat-inbox">
      <div class="chat-conv-list">
        <div class="chat-conv-list-header">
          <div class="chat-conv-list-title">Hộp Thư (Phân Loại Smart AI)</div>
        </div>
        <div class="chat-conv-items">
          ${MOCK_CHAT_SESSIONS.map((c, idx) => `
            <div class="chat-conv-item ${idx === 1 ? 'active' : ''}" onclick="window.selectChatConv(${idx})">
              <div class="chat-conv-avatar">${c.name.charAt(0)}</div>
              <div class="chat-conv-info">
                <div class="chat-conv-name">${c.name}</div>
                <div class="chat-conv-preview">${c.lastMsg}</div>
              </div>
              <div class="chat-conv-meta">
                <div class="chat-conv-time">${c.time}</div>
                <span class="chat-conv-badge ${c.type}">${c.badge}</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
      <div class="chat-detail" id="chatDetailContainer">
        </div>
    </div>
  `;
}

export function renderChatDetail(idx) {
    const conv = MOCK_CHAT_SESSIONS[idx];
    let msgsHtml = conv.messages.map(m => {
        if (m.role === 'customer') {
            return `<div class="chat-bubble customer"><div class="chat-bubble-sender">${conv.name} · ${m.time}</div>${m.text}</div>`;
        } else if (m.role === 'assistant') {
            return `<div class="chat-bubble assistant"><div class="chat-bubble-sender">AI Agent · ${m.time}</div>${m.text}</div>`;
        } else {
            return `<div class="chat-ai-suggestion">
                <div class="chat-ai-suggestion-label">🤖 Nháp AI (Dựa trên lịch sử)</div>
                <div class="chat-ai-suggestion-text" id="draftMsg-${idx}">${m.text}</div>
                <div class="chat-ai-actions">
                  <button class="btn-chat-action btn-chat-accept" onclick="window.approveChatDraft(${idx})">Gửi ngay</button>
                  <button class="btn-chat-action btn-chat-edit" onclick="window.editChatDraft(${idx})">Sửa nháp</button>
                </div>
              </div>`;
        }
    }).join('');

    return `
    <div class="chat-detail-header">
      <div class="chat-detail-title">${conv.name}</div>
    </div>
    <div class="chat-detail-messages" id="chatScroll">
      ${msgsHtml}
    </div>
    <div class="chat-detail-actions">
      <div style="display:flex; gap:10px">
        <input type="text" class="guidance-input" placeholder="Nhập tin nhắn..." ${conv.type === 'auto' ? 'disabled' : ''} />
        <button class="guidance-send-btn" ${conv.type === 'auto' ? 'disabled style="opacity:0.5"' : ''}>Gửi</button>
      </div>
    </div>
  `;
}

export function renderPoliciesHTML() {
    return `
    <div class="content-card">
      <h3 class="content-card-title">Quy Định Nền Tảng</h3>
      <div class="tab-bar">
        <button class="tab-btn active" onclick="window.switchPolicyTab('shopee', this)">Shopee</button>
        <button class="tab-btn" onclick="window.switchPolicyTab('tiktok', this)">TikTok Shop</button>
      </div>
      <h4 id="policyCardTitle" style="margin-bottom:12px; font-size:0.9rem;">Tóm tắt Quy Chế (AI)</h4>
      <div class="accordion" id="policyAccordion">
        </div>
    </div>
  `;
}

export function renderSettingsHTML() {
    return `
    <div class="grid-2">
      <div class="content-card">
        <h3 class="content-card-title">Hồ Sơ Doanh Nghiệp</h3>
        <div style="display:flex; gap:16px; align-items:center; margin-bottom:20px;">
          <div style="width:64px; height:64px; border-radius:50%; background:var(--gradient-primary); display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:bold; color:#451a03">SP</div>
          <div>
            <div style="font-weight:700; font-size:1.1rem; color:var(--text-heading);">Shop PhoneMax</div>
            <div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">Gói dịch vụ: Premium AI · ID: #88902</div>
          </div>
        </div>
        <div style="margin-bottom:16px;">
          <label style="display:block; font-size:0.8rem; color:var(--text-secondary); margin-bottom:6px;">Tông giọng Chatbot AI</label>
          <select class="guidance-input" style="width:100%; padding: 10px; background: var(--bg-secondary);">
             <option selected>Lịch sự, nhiệt tình, sử dụng nhiều emoji</option>
          </select>
        </div>
      </div>
    </div>
  `;
}
