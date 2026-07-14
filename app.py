import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)


# データベースの初期化
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating INTEGER,
            comment TEXT,
            status TEXT DEFAULT '未対応'
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


# 1. 投稿画面＆データ追加（宿泊客用）
@app.route("/", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name") or "匿名"
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)",
            (name, rating, comment),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("feedback.html")


# 2. 一覧管理画面（マネージャー用）
@app.route("/admin")
def admin():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT id, name, rating, comment, status FROM feedback")
    feedbacks = c.fetchall()
    conn.close()
    return render_template("admin.html", feedbacks=feedbacks)


# 3. ステータスを「解決済」に更新する処理
@app.route("/admin/complete/<int:feedback_id>", methods=["POST"])
def complete(feedback_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(
        "UPDATE feedback SET status = '解決済' WHERE id = ?", (feedback_id,)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)