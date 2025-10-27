// 🕒 Cập nhật đếm ngược ngày cưới
function updateCountdown() {
  const target = new Date("2025-11-30T00:00:00");
  const now = new Date();
  const diff = target - now;
  if (diff <= 0) {
    document.getElementById("countdown").innerText = "💞 Hôm nay là ngày trọng đại của chúng ta 💞";
    return;
  }
  const d = Math.floor(diff / (1000 * 60 * 60 * 24));
  const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
  const m = Math.floor((diff / (1000 * 60)) % 60);
  const s = Math.floor((diff / 1000) % 60);
  document.getElementById("countdown").innerText = `💍 Còn ${d} ngày ${h} giờ ${m} phút ${s} giây 💍`;
}
setInterval(updateCountdown, 1000);
updateCountdown();

// 💌 Gửi phản hồi và mở bản đồ / popup QR
function submitChoice(choice) {
  const guest = document.getElementById("guestName").innerText;

  // Gửi phản hồi lên server
  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guest, choice })
  });

  // Sau khi gửi phản hồi
  if (choice === "Tham gia") {
    // Mở Google Maps
    window.open("https://www.google.com/maps?q=Số+96+Đường+Thôn+6,+Bắc+Sơn,+An+Dương,+Hải+Phòng", "_blank");
  } else if (choice === "Bận - Mừng online") {
    showQrPopup();
  }
}

// 💚 Hiển thị popup mã QR ngay trên trang
function showQrPopup() {
  // Nếu popup đã tồn tại thì bỏ qua
  if (document.getElementById("qrPopup")) return;

  const overlay = document.createElement("div");
  overlay.id = "qrPopup";
  overlay.style.position = "fixed";
  overlay.style.top = 0;
  overlay.style.left = 0;
  overlay.style.width = "100%";
  overlay.style.height = "100%";
  overlay.style.background = "rgba(0,0,0,0.6)";
  overlay.style.display = "flex";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.zIndex = 9999;

  const box = document.createElement("div");
  box.style.background = "#fff";
  box.style.borderRadius = "16px";
  box.style.padding = "20px";
  box.style.textAlign = "center";
  box.style.boxShadow = "0 4px 20px rgba(0,0,0,0.4)";
  box.innerHTML = `
    <h3 style="color:#006666;">💌 Mừng cưới online 💌</h3>
    <img src="qr.jpg" alt="QR Mừng cưới" style="max-width:280px; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,0.2);">
    <p style="margin:10px 0;">Quét mã để mừng cưới nhé 🎁</p>
    <button id="closeQrBtn" style="margin-top:8px; background:#009999; color:white; border:none; padding:8px 16px; border-radius:8px; cursor:pointer;">Đóng</button>
  `;

  overlay.appendChild(box);
  document.body.appendChild(overlay);

  document.getElementById("closeQrBtn").onclick = () => overlay.remove();
}

// 💚 Hiệu ứng trái tim bay
const heartsContainer = document.getElementById("hearts-container");
function createHeart() {
  const heart = document.createElement("div");
  heart.classList.add("heart");
  const symbols = ["💗", "🌸", "🌿", "🌼", "💚"];
  heart.innerText = symbols[Math.floor(Math.random() * symbols.length)];
  heart.style.left = Math.random() * 100 + "vw";
  heart.style.animationDuration = (3 + Math.random() * 2) + "s";
  heartsContainer.appendChild(heart);
  setTimeout(() => heart.remove(), 5000);
}
setInterval(createHeart, 300);

// 🎵 Nhạc nền
const music = document.getElementById("bgMusic");
function initMusic() {
  music.play().catch(() => {});
}
