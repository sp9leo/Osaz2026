import os
import io
import json
import secrets
import zipfile
from pathlib import Path
from datetime import date
from flask import (
    Flask, request, redirect, url_for, session, render_template,
    send_from_directory, flash, send_file
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
TEACHERS_FILE = BASE_DIR / "teachers.json"

UPLOAD_DIR.mkdir(exist_ok=True)


class PrefixMiddleware:
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix.rstrip("/")

    def __call__(self, environ, start_response):
        if self.prefix:
            script_name = environ.get("SCRIPT_NAME", "")
            path_info = environ.get("PATH_INFO", "")
            if path_info.startswith(self.prefix):
                environ["SCRIPT_NAME"] = script_name + self.prefix
                environ["PATH_INFO"] = path_info[len(self.prefix):] or "/"
        return self.app(environ, start_response)


app.wsgi_app = PrefixMiddleware(app.wsgi_app, os.environ.get("PATH_PREFIX", ""))


def load_teachers():
    with open(TEACHERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def require_login(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def safe_filename(filename):
    name = secure_filename(filename)
    if not name:
        name = "report.xlsx"
    return name


def unique_path(dest_dir, filename):
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / filename
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    counter = 1
    while target.exists():
        target = dest_dir / f"{stem}_{counter}{suffix}"
        counter += 1
    return target


def list_uploads(month_filter=None):
    results = []
    if not UPLOAD_DIR.exists():
        return results
    for month_dir in sorted(UPLOAD_DIR.iterdir(), reverse=True):
        if not month_dir.is_dir():
            continue
        if month_filter and month_dir.name != month_filter:
            continue
        for teacher_dir in sorted(month_dir.iterdir()):
            if not teacher_dir.is_dir():
                continue
            for f in sorted(teacher_dir.iterdir()):
                if f.is_file():
                    results.append({
                        "month": month_dir.name,
                        "teacher": teacher_dir.name,
                        "filename": f.name,
                        "path": f"{month_dir.name}/{teacher_dir.name}/{f.name}",
                        "size": f.stat().st_size,
                    })
    return results


def available_months():
    months = []
    if not UPLOAD_DIR.exists():
        return months
    for d in sorted(UPLOAD_DIR.iterdir(), reverse=True):
        if d.is_dir():
            months.append(d.name)
    return months


MONTH_NAMES = {
    1: "Januar", 2: "Februar", 3: "Marec", 4: "April",
    5: "Maj", 6: "Junij", 7: "Julij", 8: "Avgust",
    9: "September", 10: "Oktober", 11: "November", 12: "December",
}


def allowed_upload_months():
    today = date.today()
    months = []
    for offset in range(2):
        m = today.month - offset
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        value = f"{y}-{m:02d}"
        label = f"{y} - {MONTH_NAMES[m]}"
        months.append({"value": value, "label": label})
    return months


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        config = load_teachers()
        pin = request.form.get("pin", "").strip()

        if pin == config.get("admin_pin", ""):
            session["user"] = "Administrator"
            session["is_admin"] = True
            return redirect(url_for("dashboard"))

        for t in config["teachers"]:
            if t["pin"] == pin:
                session["user"] = t["display"]
                session["teacher_name"] = t["name"]
                session["is_admin"] = False
                return redirect(url_for("dashboard"))

        flash("Napačen PIN. Poskusite znova.", "error")
        return redirect(url_for("login"))

    return render_template("index.html", login_page=True)


@app.route("/dashboard")
@require_login
def dashboard():
    config = load_teachers()
    if session.get("is_admin"):
        months = available_months()
        month = request.args.get("month", "")
        uploads = list_uploads(month_filter=month if month else None)
        return render_template(
            "index.html",
            login_page=False,
            is_admin=True,
            uploads=uploads,
            months=months,
            selected_month=month,
            teachers=config["teachers"],
        )
    else:
        my_uploads = list_uploads()
        my_uploads = [u for u in my_uploads if u["teacher"] == session.get("teacher_name")]
        return render_template(
            "index.html",
            login_page=False,
            is_admin=False,
            uploads=my_uploads,
            user=session["user"],
            upload_months=allowed_upload_months(),
        )


@app.route("/upload", methods=["POST"])
@require_login
def upload():
    if session.get("is_admin"):
        return redirect(url_for("dashboard"))

    month = request.form.get("month", "").strip()
    file = request.files.get("file")

    if not month:
        flash("Izberite mesec.", "error")
        return redirect(url_for("dashboard"))

    if not file or not file.filename:
        flash("Izberite datoteko.", "error")
        return redirect(url_for("dashboard"))

    filename = safe_filename(file.filename)
    teacher_name = session["teacher_name"]
    dest_dir = UPLOAD_DIR / month / teacher_name
    target = unique_path(dest_dir, filename)
    file.save(str(target))

    flash(f"Datoteka {target.name} je bila naložena.", "success")
    return redirect(url_for("dashboard"))


@app.route("/download/<path:filepath>")
@require_login
def download(filepath):
    parts = filepath.split("/")
    if len(parts) < 3:
        flash("Neveljavna pot.", "error")
        return redirect(url_for("dashboard"))

    if not session.get("is_admin"):
        if parts[1] != session.get("teacher_name"):
            flash("Nimate dostopa do te datoteke.", "error")
            return redirect(url_for("dashboard"))

    directory = UPLOAD_DIR / parts[0] / parts[1]
    return send_from_directory(str(directory), parts[2], as_attachment=True)


@app.route("/download_zip", methods=["POST"])
@require_login
def download_zip():
    if not session.get("is_admin"):
        flash("Nimate dostopa.", "error")
        return redirect(url_for("dashboard"))

    paths = request.form.getlist("files")
    month = request.form.get("month", "").strip()

    if not paths and month:
        uploads = list_uploads(month_filter=month)
        paths = [u["path"] for u in uploads]

    if not paths:
        flash("Ni izbranih datotek.", "error")
        return redirect(url_for("dashboard"))

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            parts = p.split("/")
            if len(parts) < 3:
                continue
            full = UPLOAD_DIR / parts[0] / parts[1] / parts[2]
            if full.is_file():
                arcname = f"{parts[0]}/{parts[1]}/{parts[2]}"
                zf.write(str(full), arcname)
    buf.seek(0)

    label = month if month else "porocila"
    return send_file(buf, mimetype="application/zip",
                     as_attachment=True, download_name=f"{label}.zip")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
