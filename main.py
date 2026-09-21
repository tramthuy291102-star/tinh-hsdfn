<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
  <!-- Cấu hình icon và tên hiển thị khi thêm ra màn hình chính -->
<link rel="apple-touch-icon" href="https://i.pinimg.com/736x/2d/7c/50/2d7c50e3dd25e3cfaa78d5a13e25576a.jpg">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Tính HSD">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Máy Tính HSD - Thùy Trâm</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
  
  * { box-sizing: border-box; touch-action: manipulation; }
  body { 
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
    background: #eef7f0; 
    padding: 15px; 
    margin: 0; 
    display: flex; 
    flex-direction: column; 
    height: 100vh;
    color: #44594a;
  }
  .card { 
    background: #ffffff; 
    padding: 15px; 
    border-radius: 24px; 
    margin-bottom: 5px; 
    box-shadow: 0 8px 24px rgba(105, 179, 131, 0.15); 
    border: 2px solid #d4edd9;
  }
  
  .today-container { text-align: center; margin-bottom: 12px; min-height: 28px;}
  .today-text { 
    display: inline-flex; align-items: center; justify-content: center; gap: 5px;
    padding: 6px 16px; background: #d4edd9; 
    color: #3b8754; border-radius: 25px; font-size: 14px; font-weight: 800; 
    cursor: pointer; transition: 0.2s; box-shadow: 0 2px 8px rgba(59, 135, 84, 0.1);
  }
  .today-text:active { background: #bce3c4; transform: scale(0.97); }

  .input-group { margin-bottom: 12px; }
  .label { font-weight: 900; margin-bottom: 6px; font-size: 15px; color: #3b8754; display: flex; align-items: center; gap: 5px;}
  
  .date-inputs, .duration-inputs { display: flex; gap: 8px; }
  .box { 
    flex: 1; 
    border: 2px dashed #bce3c4; 
    padding: 8px; 
    text-align: center; 
    border-radius: 14px; 
    font-size: 18px; 
    font-weight: 800;
    min-height: 46px; 
    color: #2c663b; 
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f7fdf8;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .box.active { border: 2px solid #5ab078; background: #d4edd9; box-shadow: 0 0 10px rgba(90, 176, 120, 0.3); transform: translateY(-2px);}
  .box:empty::before { content: attr(data-placeholder); color: #9bbfa5; font-weight: 700; font-size: 13px; }
  
  .toggle-group { display: flex; gap: 8px; margin-bottom: 10px; }
  .toggle-btn { 
    flex: 1; padding: 10px; text-align: center; border-radius: 14px; 
    border: 2px solid #5ab078; color: #5ab078; font-size: 13px; font-weight: 800; transition: 0.2s;
    background: white;
  }
  .toggle-btn.active { background: #5ab078; color: white; box-shadow: 0 4px 12px rgba(90, 176, 120, 0.35);}

  .unit-btn { 
    padding: 10px; border: 2px solid #bce3c4; border-radius: 14px; font-size: 14px; font-weight: 800; flex: 1; text-align: center; color: #5ab078; background: white; transition: 0.2s;
  }
  .unit-btn.active { background: #5ab078; color: white; border-color: #5ab078; box-shadow: 0 4px 12px rgba(90, 176, 120, 0.35);}
  
  /* Keyboard */
  .keyboard { 
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; 
    margin-top: auto; padding-bottom: 10px; 
  }
  .key { 
    background: #ffffff; border: 2px solid #eef7f0; border-radius: 16px; padding: 12px; 
    font-size: 20px; font-weight: 800; box-shadow: 0 3px 10px rgba(105, 179, 131, 0.1); color: #44594a; 
    transition: 0.1s; font-family: 'Nunito', sans-serif;
  }
  .key:active { background: #d4edd9; transform: translateY(3px); box-shadow: 0 0px 2px rgba(105, 179, 131, 0.1);}
  .key.action { background: #fff5f5; border-color: #ffe0e0; font-size: 16px; color: #ff6b6b; }
  .key.action:active { background: #ffe0e0; }
  .key.next { background: #e0f2fe; border-color: #bae6fd; font-size: 16px; color: #0284c7; }
  .key.next:active { background: #bae6fd; }
  .key.calc { background: #5ab078; border-color: #5ab078; color: white; font-size: 18px; box-shadow: 0 4px 12px rgba(90, 176, 120, 0.4);}
  .key.calc:active { background: #4a9965; transform: translateY(3px); }
  
  #result { text-align: center; font-size: 15px; font-weight: 800; padding: 12px; margin-top: 8px; border-radius: 14px; line-height: 1.4; border: 2px dashed transparent;}
  .ok { color: #2c663b; background: #d4edd9; border-color: #5ab078 !important;}
  .warn { color: #d97706; background: #fef3c7; border-color: #f59e0b !important;}
  .danger { color: #e11d48; background: #ffe4e6; border-color: #fb7185 !important;}
  .neutral { color: #64748b; background: #f1f5f9; border-color: #cbd5e1 !important;}

  .signature {
    text-align: center;
    font-family: 'Nunito', sans-serif;
    font-size: 16px;
    font-weight: 900;
    color: #5ab078;
    margin-top: 6px;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 0px #fff;
  }
</style>
</head>
<body>

<div class="card">
  <!-- Mốc Hôm Nay -->
  <div class="today-container">
    <div class="today-text" id="todayText" onclick="toggleEditToday()">
      📅 Mốc tính: --/--/---- ✏️
    </div>
    <div class="date-inputs" id="today_edit_view" style="display: none; padding-bottom: 5px;">
      <div class="box" id="today_d" onclick="setActive('today_d')" data-placeholder="Ngày"></div>
      <div class="box" id="today_m" onclick="setActive('today_m')" data-placeholder="Tháng"></div>
      <div class="box" id="today_y" onclick="setActive('today_y')" data-placeholder="Năm"></div>
    </div>
  </div>
  
  <div class="input-group">
    <div class="label">🌱 Ngày Sản Xuất (NSX)</div>
    <div class="date-inputs">
      <div class="box active" id="nsx_d" onclick="setActive('nsx_d')" data-placeholder="Ngày"></div>
      <div class="box" id="nsx_m" onclick="setActive('nsx_m')" data-placeholder="Tháng"></div>
      <div class="box" id="nsx_y" onclick="setActive('nsx_y')" data-placeholder="Năm"></div>
    </div>
  </div>

  <div class="input-group" style="margin-bottom: 2px;">
    <div class="toggle-group">
      <div class="toggle-btn active" id="mode_date" onclick="setMode('date')">🌸 Nhập ngày HSD</div>
      <div class="toggle-btn" id="mode_duration" onclick="setMode('duration')">⏳ Nhập thời hạn</div>
    </div>

    <!-- Mode: Date -->
    <div class="date-inputs" id="hsd_date_view">
      <div class="box" id="hsd_d" onclick="setActive('hsd_d')" data-placeholder="Ngày"></div>
      <div class="box" id="hsd_m" onclick="setActive('hsd_m')" data-placeholder="Tháng"></div>
      <div class="box" id="hsd_y" onclick="setActive('hsd_y')" data-placeholder="Năm"></div>
    </div>
    
    <!-- Mode: Duration -->
    <div class="duration-inputs" id="hsd_duration_view" style="display: none;">
      <div class="box" id="dur_val" onclick="setActive('dur_val')" data-placeholder="Số lượng" style="flex: 2;"></div>
      <div class="unit-btn active" id="unit_day" onclick="setUnit('day')">Ngày</div>
      <div class="unit-btn" id="unit_month" onclick="setUnit('month')">Tháng</div>
    </div>
  </div>
  
  <div id="result" class="neutral">Nhập số xong bấm TÍNH nào... ✨</div>
</div>

<div class="signature">✨ Made by Thùy Trâm ✨</div>

<!-- Numpad -->
<div class="keyboard">
  <button class="key" onclick="press('1')">1</button>
  <button class="key" onclick="press('2')">2</button>
  <button class="key" onclick="press('3')">3</button>
  <button class="key" onclick="press('4')">4</button>
  <button class="key" onclick="press('5')">5</button>
  <button class="key" onclick="press('6')">6</button>
  <button class="key" onclick="press('7')">7</button>
  <button class="key" onclick="press('8')">8</button>
  <button class="key" onclick="press('9')">9</button>
  <button class="key action" onclick="press('del')">Xóa</button>
  <button class="key" onclick="press('0')">0</button>
  <button class="key next" onclick="press('next')">Tiếp ➡️</button>
  <button class="key calc" onclick="calculate()" style="grid-column: span 3;">TÍNH 💚</button>
</div>

<script>
  let activeBox = 'nsx_d';
  let mode = 'date';
  let unit = 'day';

  let t = new Date();
  let td = t.getDate().toString().padStart(2, '0');
  let tm = (t.getMonth()+1).toString().padStart(2, '0');
  let ty = t.getFullYear().toString();
  
  document.getElementById('today_d').innerText = td;
  document.getElementById('today_m').innerText = tm;
  document.getElementById('today_y').innerText = ty;
  document.getElementById('todayText').innerHTML = `📅 Mốc tính: ${td}/${tm}/${ty} ✏️`;

  function toggleEditToday() {
    document.getElementById('todayText').style.display = 'none';
    document.getElementById('today_edit_view').style.display = 'flex';
    setActive('today_d');
  }

  function setActive(id) {
    document.querySelectorAll('.box').forEach(b => b.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    activeBox = id;
  }

  function setMode(m) {
    mode = m;
    document.getElementById('mode_date').classList.remove('active');
    document.getElementById('mode_duration').classList.remove('active');
    document.getElementById('mode_'+m).classList.add('active');
    
    if (m === 'date') {
      document.getElementById('hsd_date_view').style.display = 'flex';
      document.getElementById('hsd_duration_view').style.display = 'none';
      setActive('hsd_d');
    } else {
      document.getElementById('hsd_date_view').style.display = 'none';
      document.getElementById('hsd_duration_view').style.display = 'flex';
      setActive('dur_val');
    }
  }

  function setUnit(u) {
    unit = u;
    document.getElementById('unit_day').classList.remove('active');
    document.getElementById('unit_month').classList.remove('active');
    document.getElementById('unit_'+u).classList.add('active');
  }

  // Strict validation rules for real-time typing
  function press(val) {
    if (val === 'next') {
      moveToNextBox();
      return;
    }

    let box = document.getElementById(activeBox);
    if (val === 'del') {
      box.innerText = box.innerText.slice(0, -1);
      return;
    }

    let currentVal = box.innerText;
    let nextVal = currentVal + val;
    let isYear = activeBox.endsWith('_y');
    let isMonth = activeBox.endsWith('_m');
    let isDay = activeBox.endsWith('_d');

    if (isMonth) {
      let mNum = parseInt(nextVal);
      // Month must be 01-12. If user types e.g. '9', it's okay if next could be valid, but if first digit is > 1, invalid. 
      // If length is 1 and digit > 1 (like 2-9), it can't be a valid month unless prefixed with 0, or we can restrict: first digit > 1 is invalid for month.
      if (currentVal === '' && parseInt(val) > 1) {
        // Automatically prepend '0' if they type 2-9 for month? Or block? Let's block or auto-format. Better yet, block invalid values:
        // Month max is 12.
      }
      if (mNum > 12) return; // Ignore input if > 12
    }

    if (isDay) {
      let dNum = parseInt(nextVal);
      if (dNum > 31) return; // Day max is 31
    }

    let maxLen = isYear ? 4 : (isMonth || isDay ? 2 : (activeBox === 'dur_val' ? 5 : 2));
    if (currentVal.length < maxLen) {
      box.innerText = nextVal;
    }

    // Auto move to next box when filled max length
    if (box.innerText.length === maxLen && activeBox !== 'dur_val') {
       // Extra safety check for month when 2 digits are filled
       if (isMonth) {
         let m = parseInt(box.innerText);
         if (m < 1 || m > 12) {
           box.innerText = '';
           return;
         }
       }
       moveToNextBox();
    }
  }

  function moveToNextBox() {
     let sequence = [];
     let isTodayVisible = document.getElementById('today_edit_view').style.display === 'flex';
     
     if (isTodayVisible && (activeBox.startsWith('today'))) {
         sequence = ['today_d', 'today_m', 'today_y', 'nsx_d', 'nsx_m', 'nsx_y'];
     } else if (mode === 'date') {
         sequence = ['nsx_d', 'nsx_m', 'nsx_y', 'hsd_d', 'hsd_m', 'hsd_y'];
     } else {
         sequence = ['nsx_d', 'nsx_m', 'nsx_y', 'dur_val'];
     }
     
     let idx = sequence.indexOf(activeBox);
     if (idx !== -1 && idx < sequence.length - 1) {
         setActive(sequence[idx+1]);
     }
  }

  function parseMyDate(d, m, y) {
    let dv = parseInt(d), mv = parseInt(m), yv = parseInt(y);
    if (isNaN(dv) || isNaN(mv) || isNaN(yv)) return null;
    if (yv < 100) yv += 2000;
    
    // Strict calendar check
    if (mv < 1 || mv > 12) return null;
    if (dv < 1 || dv > 31) return null;
    
    let dateObj = new Date(yv, mv - 1, dv);
    // Check if JS Date rolled over (e.g., Feb 31 becomes March 3)
    if (dateObj.getFullYear() !== yv || dateObj.getMonth() !== mv - 1 || dateObj.getDate() !== dv) {
      return null;
    }
    return dateObj;
  }

  function calculate() {
    let nsx = parseMyDate(
      document.getElementById('nsx_d').innerText,
      document.getElementById('nsx_m').innerText,
      document.getElementById('nsx_y').innerText
    );
    if (!nsx) {
      showResult("Ngày Sản Xuất không hợp lệ (ví dụ: ngày quá 31 hoặc tháng quá 12)! 🥺", "danger"); return;
    }

    let hsd = null;
    if (mode === 'date') {
      hsd = parseMyDate(
        document.getElementById('hsd_d').innerText,
        document.getElementById('hsd_m').innerText,
        document.getElementById('hsd_y').innerText
      );
      if (!hsd) {
        showResult("Hạn Sử Dụng không hợp lệ! 🥺", "danger"); return;
      }
    } else {
      let dur = parseInt(document.getElementById('dur_val').innerText);
      if (isNaN(dur) || dur < 0) {
         showResult("Chưa nhập số thời hạn hợp lệ kìa! 🥺", "danger"); return;
      }
      hsd = new Date(nsx.getTime());
      if (unit === 'day') {
        // Nếu cộng ngày, ví dụ cộng 1 ngày từ NSX thì HSD = NSX + 1 ngày. Nhưng vì tính luôn NSX là 1 ngày SD, 
        // nên nếu thời hạn là X ngày, ngày cuối cùng sẽ là NSX + (X - 1) ngày.
        hsd.setDate(hsd.getDate() + dur - 1);
      } else {
        hsd.setMonth(hsd.getMonth() + dur);
        // Trừ đi 1 ngày vì tính nguyên vẹn tháng/ngày có tính ngày NSX
        hsd.setDate(hsd.getDate() - 1);
      }
    }

    let todayDate = parseMyDate(
      document.getElementById('today_d').innerText,
      document.getElementById('today_m').innerText,
      document.getElementById('today_y').innerText
    );
    if (!todayDate) {
      showResult("Mốc thời gian tính không hợp lệ! 🥺", "danger"); return;
    }

    todayDate.setHours(0,0,0,0);
    nsx.setHours(0,0,0,0);
    hsd.setHours(0,0,0,0);

    // Tính luôn ngày NSX là 1 ngày sử dụng -> Tổng số ngày = (HSD - NSX) + 1
    let diffTime = hsd.getTime() - nsx.getTime();
    let totalDays = Math.round(diffTime / (1000 * 60 * 60 * 24)) + 1;

    if (totalDays <= 0) {
       showResult("Hình như HSD đang nhỏ hơn NSX nè! 🤔", "danger");
       return;
    }

    let remainingTime = hsd.getTime() - todayDate.getTime();
    let remainingDays = Math.round(remainingTime / (1000 * 60 * 60 * 24)) + 1;

    let percent = (remainingDays / totalDays) * 100;
    
    let formattedHSD = `${hsd.getDate().toString().padStart(2,'0')}/${(hsd.getMonth()+1).toString().padStart(2,'0')}/${hsd.getFullYear()}`;
    
    if (percent <= 0 || remainingDays <= 0) {
       let expiredDays = Math.abs(remainingDays - 1);
       showResult(`❌ ĐÃ QUÁ HẠN RỒI!<br><span style="font-size:13px; font-weight:700;">(Đã hết hạn vào: ${formattedHSD})</span>`, "danger");
    } else {
       let typeClass = percent > 30 ? 'ok' : 'warn';
       let icon = percent > 30 ? '✅' : '⚠️';
       showResult(`${icon} Còn lại: ${percent.toFixed(1)}% (~${remainingDays} ngày)<br><span style="font-size:13px; font-weight:700;">(Tính luôn ngày NSX, HSD là ${formattedHSD})</span>`, typeClass);
    }
  }

  function showResult(msg, type) {
     let r = document.getElementById('result');
     r.innerHTML = msg;
     r.className = type;
  }
</script>

<!-- ============================================================ -->
<!-- ===   PHẦN THÊM MỚI: LƯU SẢN PHẨM & CẢNH BÁO NGÀY RÚT     === -->
<!-- ===   Không chỉnh sửa bất kỳ code nào phía trên            === -->
<!-- ============================================================ -->

<style>
  /* Banner cảnh báo trên cùng */
  #hsdAlertBanner {
    position: fixed;
    top: max(10px, env(safe-area-inset-top));
    left: 50%;
    transform: translateX(-50%);
    max-width: calc(100% - 30px);
    width: 420px;
    background: #fff3cd;
    color: #92400e;
    border: 2px solid #f59e0b;
    border-radius: 14px;
    padding: 10px 14px;
    font-weight: 800;
    font-size: 13px;
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.35);
    z-index: 9998;
    display: none;
    cursor: pointer;
    animation: hsdSlideDown 0.4s ease;
    text-align: center;
    line-height: 1.5;
  }
  #hsdAlertBanner.danger {
    background: #ffe4e6;
    color: #9f1239;
    border-color: #fb7185;
    box-shadow: 0 6px 20px rgba(251, 113, 133, 0.35);
  }
  @keyframes hsdSlideDown {
    from { opacity: 0; transform: translate(-50%, -20px); }
    to   { opacity: 1; transform: translate(-50%, 0); }
  }

  /* Nút nổi mở danh sách */
  #hsdFloatBtn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: #5ab078;
    color: white;
    border: 3px solid white;
    box-shadow: 0 6px 20px rgba(90, 176, 120, 0.5);
    font-size: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9997;
    cursor: pointer;
    transition: transform 0.15s;
    font-family: 'Nunito', sans-serif;
  }
  #hsdFloatBtn:active { transform: scale(0.9); }
  #hsdFloatBtn .badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #ff6b6b;
    color: white;
    font-size: 11px;
    font-weight: 900;
    min-width: 20px;
    height: 20px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 5px;
    border: 2px solid white;
  }

  /* Nút Lưu sản phẩm (chèn sau #result) */
  #hsdSaveBtn {
    display: none;
    width: 100%;
    margin-top: 8px;
    padding: 10px 18px;
    background: #0284c7;
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 800;
    font-size: 14px;
    font-family: 'Nunito', sans-serif;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    cursor: pointer;
    transition: transform 0.1s;
  }
  #hsdSaveBtn:active { transform: translateY(2px); }

  /* Modal danh sách */
  #hsdModal {
    position: fixed;
    inset: 0;
    background: rgba(30, 50, 40, 0.5);
    z-index: 9999;
    display: none;
    align-items: flex-end;
    justify-content: center;
    backdrop-filter: blur(3px);
  }
  #hsdModal.open { display: flex; }
  #hsdModalContent {
    background: #fff;
    width: 100%;
    max-width: 500px;
    max-height: 82vh;
    border-radius: 24px 24px 0 0;
    padding: 18px;
    overflow-y: auto;
    animation: hsdSlideUp 0.3s ease;
    border: 2px solid #d4edd9;
    border-bottom: none;
    font-family: 'Nunito', sans-serif;
  }
  @keyframes hsdSlideUp {
    from { transform: translateY(100%); }
    to   { transform: translateY(0); }
  }
  .hsdModalHeader {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .hsdModalHeader h2 {
    font-size: 18px;
    color: #3b8754;
    margin: 0;
    font-weight: 900;
  }
  .hsdCloseBtn {
    background: #ffe4e6;
    color: #e11d48;
    border: none;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    font-size: 16px;
    font-weight: 900;
    cursor: pointer;
    font-family: inherit;
  }
  .hsdItem {
    background: #f7fdf8;
    border: 2px solid #d4edd9;
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 10px;
    position: relative;
  }
  .hsdItem.expired { background: #ffe4e6; border-color: #fb7185; }
  .hsdItem.urgent  {
    background: #ffedd5;
    border-color: #fb923c;
    box-shadow: inset 0 0 0 1px rgba(251, 146, 60, 0.3);
  }
  .hsdItem.urgent .hsdItemName { color: #9a3412; }
  .hsdItem.soon    { background: #fef3c7; border-color: #f59e0b; }
  .hsdItemName {
    font-weight: 900;
    color: #2c663b;
    font-size: 15px;
    margin-bottom: 4px;
    padding-right: 40px;
    word-break: break-word;
  }
  .hsdItemInfo {
    font-size: 12.5px;
    color: #44594a;
    font-weight: 700;
    line-height: 1.6;
  }
  .hsdItemDelete {
    position: absolute;
    top: 8px;
    right: 8px;
    background: #ffe4e6;
    color: #e11d48;
    border: none;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-weight: 900;
    cursor: pointer;
    font-family: inherit;
  }
  .hsdEmpty {
    text-align: center;
    color: #9bbfa5;
    font-weight: 800;
    padding: 30px 10px;
    line-height: 1.8;
  }
</style>

<!-- Banner cảnh báo (bấm để mở danh sách) -->
<div id="hsdAlertBanner" onclick="openHsdModal()"></div>

<!-- Nút nổi mở danh sách sản phẩm đã lưu -->
<div id="hsdFloatBtn" onclick="openHsdModal()">
  📦
  <span class="badge" id="hsdBadge" style="display:none;">0</span>
</div>

<!-- Modal danh sách -->
<div id="hsdModal" onclick="if(event.target===this) closeHsdModal()">
  <div id="hsdModalContent">
    <div class="hsdModalHeader">
      <h2>📦 Sản phẩm đã lưu</h2>
      <button class="hsdCloseBtn" onclick="closeHsdModal()">✕</button>
    </div>
    <div id="hsdList"></div>
  </div>
</div>

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
<!-- ==================== HẾT PHẦN THÊM MỚI ==================== -->
</body>
</html>
