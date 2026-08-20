"""
Build the Assignment 1 submission PDF.

Assembles:
  - Title page + requirements checklist
  - Screenshots of the running application
  - Syntax-highlighted source code listings
into a single HTML document, then renders it to PDF with Chromium (Playwright).

Usage:
    python build_report.py
Optional: set the GitHub URL once the repo is pushed:
    python build_report.py --github https://github.com/you/movie-watchlist
"""
import argparse
import base64
import os

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, HtmlDjangoLexer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(BASE_DIR, "screenshots")
OUT_HTML = os.path.join(BASE_DIR, "Assignment1_Submission.html")
OUT_PDF = os.path.join(BASE_DIR, "Assignment1_Submission.pdf")

STUDENT = "st126005@ait.asia"
COURSE = "AST02.04 Full Stack Application Development · FSAD 2026"

# --- Screenshots (file, caption) in order ------------------------------------
SCREENSHOTS = [
    ("01_homepage.png", "Homepage — lists all movies ordered newest first, with "
     "genre, release year, star rating, Watched/Unwatched status badges, and "
     "per-row actions."),
    ("02_search.png", "Search by title — filtering the list with the query "
     "“dune” returns only the matching movie (case-insensitive)."),
    ("03_add_form.png", "Add Movie — the create form (ModelForm) for a new entry."),
    ("04_validation.png", "Server-side validation — submitting an empty title and "
     "a rating of 9 is rejected: “This field is required” and "
     "“Ensure this value is less than or equal to 5”."),
    ("05_edit_form.png", "Edit Movie — the update form pre-populated with the "
     "existing movie's data."),
    ("06_delete_confirm.png", "Delete confirmation — deletion requires an explicit "
     "confirmation (POST), preventing accidental removal."),
    ("07_admin_login.png", "Django Admin — the built-in admin login page."),
    ("08_admin_movies.png", "Django Admin — the Movie model registered with a "
     "custom list display, “By watched” and “By genre” filters, "
     "search, and inline editable Watched field."),
    ("09_admin_movie_detail.png", "Django Admin — the Movie change form."),
]

# --- Code listings (file, caption) -------------------------------------------
CODE_FILES = [
    ("movies/models.py", "The Movie model — all six required fields with "
     "validation and newest-first ordering."),
    ("movies/forms.py", "MovieForm — a ModelForm shared by the add and edit views."),
    ("movies/views.py", "Views — CRUD, search, and the watched-toggle, using the "
     "Django ORM."),
    ("movies/urls.py", "App-level URL routing."),
    ("config/urls.py", "Project-level URL routing."),
    ("movies/admin.py", "Registering the Movie model in the Django Admin."),
    ("config/settings.py", "Project settings — installed apps, templates, and the "
     "PostgreSQL database configuration (secrets read from a .env file)."),
    ("movies/tests.py", "Automated tests for the model and the views (9 tests)."),
    ("templates/movies/movie_list.html", "The homepage template (Django Template "
     "Language + Bootstrap)."),
]

REQUIREMENTS = [
    ("Homepage listing all movies", "movie_list view + movie_list.html"),
    ("Movies ordered by newest first", "Meta.ordering = ['-date_added']"),
    ("Add a new movie", "movie_create view"),
    ("Edit an existing movie", "movie_update view"),
    ("Delete a movie (with confirmation)", "movie_delete view"),
    ("Mark a movie as Watched / Unwatched", "movie_toggle_watched view"),
    ("Search by movie title", "?q= filter (title__icontains)"),
    ("Title required; Rating 1–5 validated", "model validators + ModelForm"),
    ("Django + PostgreSQL, using the ORM", "settings.DATABASES + QuerySets"),
    ("CRUD functionality", "create / read / update / delete"),
    ("HTML templates (Bootstrap)", "templates/ + Bootstrap 5"),
    ("Movie registered in Django Admin", "movies/admin.py"),
    ("Automated tests", "9/9 passing"),
    ("Git version control", "repository + commit history"),
]


def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def code_html(rel_path):
    full = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
    with open(full, encoding="utf-8") as f:
        src = f.read()
    lexer = HtmlDjangoLexer() if rel_path.endswith(".html") else PythonLexer()
    formatter = HtmlFormatter(nowrap=False, style="friendly", linenos="table")
    return highlight(src, lexer, formatter)


def build(github_url):
    pyg_css = HtmlFormatter(style="friendly").get_style_defs(".highlight")

    parts = []
    parts.append(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    @page {{ size: A4; margin: 16mm 14mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1a1a1a;
           font-size: 12px; line-height: 1.5; }}
    h1 {{ font-size: 26px; margin: 0 0 4px; }}
    h2 {{ font-size: 18px; border-bottom: 2px solid #0d6efd; padding-bottom: 4px;
          margin-top: 28px; color: #0d3b82; }}
    h3 {{ font-size: 14px; margin: 18px 0 6px; color: #222; }}
    .cover {{ text-align: center; padding-top: 120px; }}
    .cover .emoji {{ font-size: 64px; }}
    .cover .sub {{ color: #555; font-size: 15px; margin-top: 8px; }}
    .meta {{ margin-top: 40px; font-size: 13px; color: #333; }}
    .pagebreak {{ page-break-before: always; }}
    table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
    th, td {{ border: 1px solid #cfd8e3; padding: 5px 8px; text-align: left;
             font-size: 11px; vertical-align: top; }}
    th {{ background: #0d3b82; color: #fff; }}
    tr:nth-child(even) td {{ background: #f4f7fb; }}
    .ok {{ color: #157347; font-weight: bold; }}
    figure {{ margin: 6px 0 18px; page-break-inside: avoid; }}
    figure img {{ width: 100%; border: 1px solid #ccc; border-radius: 4px; }}
    figcaption {{ font-size: 11px; color: #444; margin-top: 5px; font-style: italic; }}
    .codecard {{ page-break-inside: avoid; margin-bottom: 18px; }}
    .highlighttable {{ width: 100%; font-size: 9.5px; }}
    .highlight pre {{ margin: 0; font-family: 'Consolas','Courier New',monospace;
                      white-space: pre-wrap; word-break: break-word; }}
    .linenos {{ color: #999; padding-right: 8px; user-select: none; }}
    .codecap {{ font-size: 11px; color: #444; margin: 2px 0 6px; font-style: italic; }}
    .ghbox {{ border: 2px dashed #0d6efd; padding: 12px 16px; border-radius: 6px;
             background: #eef4ff; font-size: 13px; }}
    code {{ background:#eef1f5; padding:1px 4px; border-radius:3px;
            font-family:'Consolas',monospace; }}
    {pyg_css}
    </style></head><body>""")

    # Cover
    parts.append(f"""<div class="cover">
      <div class="emoji">\U0001F3AC</div>
      <h1>Movie Watchlist</h1>
      <div class="sub">Django + PostgreSQL Web Application</div>
      <div class="meta">
        <strong>Assignment 1</strong><br>
        {COURSE}<br>
        Student: {STUDENT}<br>
        Stack: Python 3.13 · Django 6.0 · PostgreSQL 18 · Bootstrap 5
      </div>
    </div>""")

    # Requirements checklist
    rows = "".join(
        f"<tr><td>{r}</td><td>{impl}</td><td class='ok'>&#10003;</td></tr>"
        for r, impl in REQUIREMENTS
    )
    parts.append(f"""<div class="pagebreak"></div>
      <h2>1. Requirements Checklist</h2>
      <p>Every functional and technical requirement from the assignment brief,
      and where it is implemented. All items were verified in the running
      application.</p>
      <table><tr><th>Requirement</th><th>Implemented by</th><th>Done</th></tr>
      {rows}</table>""")

    # GitHub URL box
    gh = github_url or ("&lt;add your GitHub repository URL here after pushing&gt; "
                        "&mdash; e.g. https://github.com/your-username/movie-watchlist")
    parts.append(f"""<h3>GitHub Repository</h3>
      <div class="ghbox">{gh}</div>""")

    # Screenshots
    parts.append('<div class="pagebreak"></div><h2>2. Application Screenshots</h2>')
    for fname, cap in SCREENSHOTS:
        fpath = os.path.join(SHOTS, fname)
        if not os.path.exists(fpath):
            continue
        b64 = img_b64(fpath)
        parts.append(
            f'<figure><img src="data:image/png;base64,{b64}">'
            f'<figcaption>{cap}</figcaption></figure>'
        )

    # Code listings
    parts.append('<div class="pagebreak"></div><h2>3. Source Code</h2>')
    for rel, cap in CODE_FILES:
        parts.append(
            f'<div class="codecard"><h3>{rel}</h3>'
            f'<div class="codecap">{cap}</div>{code_html(rel)}</div>'
        )

    parts.append("</body></html>")
    html = "".join(parts)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    # Render to PDF
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.goto("file:///" + OUT_HTML.replace(os.sep, "/"))
        page.pdf(path=OUT_PDF, format="A4",
                 margin={"top": "16mm", "bottom": "16mm",
                         "left": "14mm", "right": "14mm"},
                 print_background=True)
        b.close()
    print("PDF written:", OUT_PDF)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--github", default="", help="GitHub repository URL")
    args = ap.parse_args()
    build(args.github)
