from flask import Flask, request, render_template_string, jsonify, send_from_directory, make_response
import os, datetime
import csv  # <-- SỬA LỖI 1: Thêm import csv

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "guests.csv")

# Tạo thư mục data và file CSV nếu chưa có
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "guest", "choice"])

@app.route("/")
def index():
    guest = request.args.get("guest", "Bạn thân thương").replace("-", " ")
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html, guest_name=guest)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    guest = data.get("guest", "Không rõ")
    choice = data.get("choice", "Không rõ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, guest, choice])
    return jsonify({"status": "ok"})

@app.route("/admin")
def admin():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    table_rows = "".join([
        f"<tr><td>{r['timestamp']}</td><td>{r['guest']}</td><td>{r['choice']}</td></tr>"
        for r in rows
    ])
    return f"""
    <html>
    <head>
      <meta charset="utf-8">
      <title>Danh sách khách mời</title>
      <style>
        body {{ font-family: Arial; background: #e6f9f9; color:#004d4d; text-align:center; }}
        table {{ margin:auto; border-collapse: collapse; width:90%; max-width:800px; }}
        th, td {{ border:1px solid #009999; padding:8px; }}
        th {{ background:#00cccc; color:white; }}
      </style>
    </head>
    <body>
      <h2>📋 Danh sách phản hồi khách mời</h2>
      <table>
        <tr><th>Thời gian</th><th>Khách mời</th><th>Lựa chọn</th></tr>
        {table_rows or '<tr><td colspan=3>Chưa có phản hồi nào</td></tr>'}
      </table>
    </body>
    </html>
    """

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

# SỬA LỖI 2: Di chuyển hàm này lên TRƯỚC app.run()
@app.after_request
def skip_ngrok_warning(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)