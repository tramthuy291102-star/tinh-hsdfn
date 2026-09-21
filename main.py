<script>
/* ============================================================
   MODULE ĐỘC LẬP - KHÔNG CHỈNH SỬA CODE CŨ
   - Lưu sản phẩm vào localStorage
   - Cảnh báo theo % THỜI HẠN còn lại: 2 mức (30% & 20%)
   ============================================================ */
(function () {
  const STORAGE_KEY    = 'hsd_saved_products_v1';
  const SOON_PERCENT   = 30;  // ⚠️ Ngưỡng "sắp hết hạn"
  const URGENT_PERCENT = 20;  // 🚨 Ngưỡng "rất gấp"

  // ---------- Tiện ích ----------
  function load() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch { return []; }
  }
  function save(list) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  }
  function parseVN(s) {
    if (!s) return null;
    const parts = String(s).split('/').map(Number);
    if (parts.length !== 3) return null;
    const [d, m, y] = parts;
    if (!d || !m || !y) return null;
    return new Date(y, m - 1, d);
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => (
      { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]
    ));
  }

  // ---------- Tính % thời hạn còn lại ----------
  function percentLeft(nsxStr, hsdStr, today) {
    const nsx = parseVN(nsxStr);
    const hsd = parseVN(hsdStr);
    if (!nsx || !hsd) return null;

    nsx.setHours(0,0,0,0);
    hsd.setHours(0,0,0,0);
    const t = new Date(today); t.setHours(0,0,0,0);

    const total = Math.round((hsd - nsx) / 86400000) + 1;
    if (total <= 0) return null;

    const remain = Math.round((hsd - t) / 86400000) + 1;
    const percent = (remain / total) * 100;
    const expiredDays = remain <= 0 ? Math.abs(remain) + 1 : 0;

    return { total, remain, percent, expiredDays };
  }

  // ---------- Phân loại mức độ ----------
  function getLevel(info) {
    if (!info)               return 'unknown';
    if (info.remain <= 0)    return 'expired';
    if (info.percent <= URGENT_PERCENT) return 'urgent';
    if (info.percent <= SOON_PERCENT)   return 'soon';
    return 'safe';
  }

  // ---------- Tạo nút Lưu ----------
  const saveBtn = document.createElement('button');
  saveBtn.id = 'hsdSaveBtn';
  saveBtn.type = 'button';
  saveBtn.innerText = '💾 Lưu sản phẩm này';
  const resultEl = document.getElementById('result');
  resultEl.parentNode.insertBefore(saveBtn, resultEl.nextSibling);

  // ---------- Bọc hàm showResult gốc ----------
  let pendingData = null;
  const origShowResult = window.showResult;

  window.showResult = function (msg, type) {
    origShowResult(msg, type);
    try {
      if (type === 'ok' || type === 'warn') {
        const nsx_d = document.getElementById('nsx_d').innerText;
        const nsx_m = document.getElementById('nsx_m').innerText;
        const nsx_y = document.getElementById('nsx_y').innerText;

        let hsdStr = '';
        const m = String(msg).match(/HSD là (\d{2}\/\d{2}\/\d{4})/);
        if (m) hsdStr = m[1];
        else {
          const hd = document.getElementById('hsd_d').innerText;
          const hm = document.getElementById('hsd_m').innerText;
          const hy = document.getElementById('hsd_y').innerText;
          if (hd && hm && hy) hsdStr = `${hd}/${hm}/${hy}`;
        }

        if (nsx_d && nsx_m && nsx_y && hsdStr) {
          pendingData = { nsx: `${nsx_d}/${nsx_m}/${nsx_y}`, hsd: hsdStr };
          saveBtn.innerText = '💾 Lưu sản phẩm này';
          saveBtn.style.display = 'block';
          return;
        }
      }
      pendingData = null;
      saveBtn.style.display = 'none';
    } catch (e) { console.warn('[HSD save]', e); }
  };

  // ---------- Lưu sản phẩm ----------
  saveBtn.onclick = function () {
    if (!pendingData) return;
    const defName = 'SP ' + new Date().toLocaleString('vi-VN');
    const name = prompt('Đặt tên cho sản phẩm (VD: Son MAC, Serum...):', defName);
    if (name === null) return;

    const list = load();
    list.unshift({
      id: Date.now() + Math.floor(Math.random() * 1000),
      name: (name.trim() || defName),
      nsx: pendingData.nsx,
      hsd: pendingData.hsd,
      savedAt: Date.now()
    });
    save(list);

    saveBtn.innerText = '✅ Đã lưu vào danh sách!';
    setTimeout(() => {
      saveBtn.style.display = 'none';
      saveBtn.innerText = '💾 Lưu sản phẩm này';
    }, 1400);

    renderBadge();
    renderAlert();
    if (document.getElementById('hsdModal').classList.contains('open')) renderList();
  };

  // ---------- Modal ----------
  window.openHsdModal = function () {
    document.getElementById('hsdModal').classList.add('open');
    renderList();
  };
  window.closeHsdModal = function () {
    document.getElementById('hsdModal').classList.remove('open');
  };

  // ---------- Render danh sách ----------
  function renderList() {
    const list = load();
    const box = document.getElementById('hsdList');
    if (!list.length) {
      box.innerHTML = '<div class="hsdEmpty">Chưa có sản phẩm nào được lưu 🌱<br>' +
                      '<span style="font-size:12px;">Tính HSD xong, bấm "💾 Lưu sản phẩm này" nhé!</span></div>';
      return;
    }
    const today = new Date();

    // Sắp xếp: gấp nhất lên đầu
    const order = { expired: 0, urgent: 1, soon: 2, safe: 3, unknown: 4 };
    const sorted = list.slice().sort((a, b) => {
      const la = getLevel(percentLeft(a.nsx, a.hsd, today));
      const lb = getLevel(percentLeft(b.nsx, b.hsd, today));
      return order[la] - order[lb];
    });

    box.innerHTML = sorted.map(item => {
      const info  = percentLeft(item.nsx, item.hsd, today);
      const level = getLevel(info);
      let cls = '', status = '';

      if (level === 'unknown') {
        status = '⚠️ Không đọc được ngày';
      } else if (level === 'expired') {
        cls = 'expired';
        status = `❌ Đã hết hạn ${info.expiredDays} ngày trước`;
      } else if (level === 'urgent') {
        cls = 'urgent';
        status = `🚨 RẤT GẤP! Chỉ còn ${info.percent.toFixed(1)}% (~${info.remain} ngày) — cần rút ngay!`;
      } else if (level === 'soon') {
        cls = 'soon';
        status = `⚠️ Sắp hết: còn ${info.percent.toFixed(1)}% (~${info.remain} ngày)`;
      } else {
        status = `✅ Còn ${info.percent.toFixed(1)}% (~${info.remain} ngày)`;
      }

      const saveDate = new Date(item.savedAt).toLocaleString('vi-VN');
      return `
        <div class="hsdItem ${cls}">
          <button class="hsdItemDelete" onclick="hsdDelete(${item.id})" title="Xoá">✕</button>
          <div class="hsdItemName">${escapeHtml(item.name)}</div>
          <div class="hsdItemInfo">
            🌱 NSX: ${item.nsx}<br>
            ⏰ HSD: ${item.hsd}<br>
            ${status}<br>
            <span style="font-size:11px;color:#9bbfa5;">Đã lưu: ${saveDate}</span>
          </div>
        </div>`;
    }).join('');
  }

  window.hsdDelete = function (id) {
    if (!confirm('Xoá sản phẩm này khỏi danh sách?')) return;
    const list = load().filter(x => x.id !== id);
    save(list);
    renderList();
    renderBadge();
    renderAlert();
  };

  // ---------- Badge ----------
  function renderBadge() {
    const list = load();
    const b = document.getElementById('hsdBadge');
    if (list.length) { b.style.display = 'flex'; b.innerText = list.length; }
    else b.style.display = 'none';
  }

  // ---------- Banner: hiển thị CẢ 2 LOẠI ----------
  function renderAlert() {
    const list  = load();
    const today = new Date();

    let expired = [], urgent = [], soon = [];

    list.forEach(it => {
      const info  = percentLeft(it.nsx, it.hsd, today);
      const level = getLevel(info);
      if (level === 'expired') expired.push(it);
      else if (level === 'urgent') urgent.push(it);
      else if (level === 'soon')   soon.push(it);
    });

    const banner = document.getElementById('hsdAlertBanner');
    if (!expired.length && !urgent.length && !soon.length) {
      banner.style.display = 'none';
      return;
    }
    banner.style.display = 'block';
    // Đỏ khi có expired HOẶC urgent
    banner.classList.toggle('danger', expired.length > 0 || urgent.length > 0);

    const parts = [];
    if (expired.length) parts.push(`❌ ${expired.length} SP đã hết hạn`);
    if (urgent.length)  parts.push(`🚨 ${urgent.length} SP còn < ${URGENT_PERCENT}%`);
    if (soon.length)    parts.push(`⚠️ ${soon.length} SP còn < ${SOON_PERCENT}%`);

    banner.innerText = parts.join(' • ') + ' — Bấm xem 📦';
  }

  // ---------- Khởi động ----------
  renderBadge();
  renderAlert();
  setInterval(renderAlert, 60 * 1000);

})();
</script>