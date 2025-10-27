const intro = document.getElementById("intro-screen");
const mainContent = document.querySelector(".main-content");
const music = document.getElementById("bgMusic");

// 🌸 Mở cửa + hiện dần nội dung
intro.addEventListener("click", () => {
  intro.classList.add("open");
  mainContent.classList.add("visible"); // bắt đầu fade-in cùng lúc mở cửa

  setTimeout(() => {
    intro.style.display = "none"; // ẩn hai cánh cửa sau khi mở xong
    initMusic();
  }, 1600);
});

// 🎵 Phát nhạc
function initMusic() {
  music.play().catch(() => console.log("⚠️ Cần tương tác người dùng để phát nhạc."));
}

// 💍 Đếm ngược
function updateCountdown() {
  const target = new Date("2025-11-30T00:00:00");
  const now = new Date();
  const diff = target - now;
  if (diff <= 0) {
    document.getElementById("countdown").innerText =
      "💞 Hôm nay là ngày trọng đại của chúng ta 💞";
    return;
  }
  const d = Math.floor(diff / (1000 * 60 * 60 * 24));
  const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
  const m = Math.floor((diff / (1000 * 60)) % 60);
  const s = Math.floor((diff / 1000) % 60);
  document.getElementById("countdown").innerText =
    `💍 Còn ${d} ngày ${h} giờ ${m} phút ${s} giây 💍`;
}
setInterval(updateCountdown, 1000);
updateCountdown();

// 💌 Gửi lựa chọn
function submitChoice(choice) {
  const guest = document.getElementById("guestName").innerText;
  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guest, choice }),
  });

  if (choice === "Tham gia") {
    window.open(
      "https://www.google.com/maps?q=Số+96+Đường+Thôn+6,+Bắc+Sơn,+An+Dương,+Hải+Phòng",
      "_blank"
    );
  } else if (choice === "Bận - Mừng online") {
    showQrPopup();
  }
}

// 💌 Popup QR
function showQrPopup() {
  if (document.getElementById("qrPopup")) return;
  const overlay = document.createElement("div");
  overlay.id = "qrPopup";
  overlay.innerHTML = `
    <div>
      <h3 style="color:#006666;">💌 Mừng cưới online 💌</h3>
      <img src="qr.jpg" alt="QR Mừng cưới">
      <p>Quét mã để mừng cưới nhé 🎁</p>
      <button onclick="document.getElementById('qrPopup').remove()" style="background:#009999;color:white;border:none;padding:8px 16px;border-radius:8px;">Đóng</button>
    </div>`;
  document.body.appendChild(overlay);
}
