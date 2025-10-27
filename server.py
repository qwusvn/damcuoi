from flask import Flask, request, render_template_string, jsonify, send_from_directory
import os, datetime, requests

app = Flask(__name__)

# ==== THIẾT LẬP WEBHOOK GOOGLE SHEET ====
# Dán URL bạn nhận được khi deploy Apps Script (dạng https://script.google.com/macros/s/AKfycbxxxx/exec)
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyfQ0cWcUePAqL-YdbL6WJqiaSRBk9THmr48jsO4nckppk3MZgWLdiBQf0NXqY-3ziq/exec"

# ==== CẤU HÌNH CƠ BẢN ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    guest = request.args.get("guest", "Bạn thân thương").replace("-", " ")
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html, guest_name=guest)

@app.route("/submit", methods=["POST"])
def submit():
    """Nhận phản hồi của khách và gửi tới Google Sheet"""
    data = request.get_json()
    guest = data.get("guest", "Không rõ")
    choice = data.get("choice", "Không rõ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Gửi dữ liệu qua webhook Google Sheet
    try:
        requests.post(WEBHOOK_URL, json={"guest": guest, "choice": choice})
        print(f"✅ Đã gửi: {guest} - {choice}")
    except Exception as e:
        print("❌ Lỗi gửi webhook:", e)

    # Lưu dự phòng cục bộ nếu muốn (không bắt buộc)
    local_file = os.path.join(BASE_DIR, "data_guests_backup.csv")
    try:
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        with open(local_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp},{guest},{choice}\n")
    except Exception as e:
        print("⚠️ Không thể ghi backup CSV:", e)

    return jsonify({"status": "ok"})

@app.route("/admin")
def admin():
    """Hiển thị danh sách backup cục bộ (nếu có)"""
    local_file = os.path.join(BASE_DIR, "data_guests_backup.csv")
    rows = []
    if os.path.exists(local_file):
        with open(local_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    rows.append(parts)

    table_rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows
    )

    return f"""
    <html>
    <head>
      <meta charset="utf-8">
      <title>Danh sách khách mời</title>
      <style>
        body {{ font-family: Arial; background:#e6f9f9; color:#004d4d; text-align:center; }}
        table {{ margin:auto; border-collapse:collapse; width:90%; max-width:800px; }}
        th,td {{ border:1px solid #009999; padding:8px; }}
        th {{ background:#00cccc; color:white; }}
      </style>
    </head>
    <body>
      <h2>📋 Danh sách phản hồi (backup cục bộ)</h2>
      <table>
        <tr><th>Thời gian</th><th>Khách mời</th><th>Lựa chọn</th></tr>
        {table_rows or '<tr><td colspan=3>Chưa có dữ liệu</td></tr>'}
      </table>
    </body>
    </html>
    """

@app.route("/<path:filename>")
def serve_static(filename):
    """Phục vụ file tĩnh (ảnh, CSS, JS, nhạc...)"""
    return send_from_directory(BASE_DIR, filename)

# Bỏ cảnh báo ngrok
@app.after_request
def skip_ngrok_warning(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
