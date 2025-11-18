from flask import Flask, render_template, request
from crewai_application import run_study_planner
import markdown

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reports = None
    html_reports = {} 

    if request.method == "POST":
        country = request.form.get("country")
        level = request.form.get("level")
        stream = request.form.get("stream")
        if country and level and stream:
            reports = run_study_planner(country, level, stream)
            if reports:
                for key, content in reports.items():
                    html_reports[key] = markdown.markdown(content)
                reports = html_reports

    return render_template("index.html", reports=reports)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8501,
        debug=True,
        use_reloader=False,
    )