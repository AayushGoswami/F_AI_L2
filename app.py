from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/blood_report_analyzer')
# def blood_report_analyzer():
#     return render_template('blood_report_analyzer.html')

@app.route('/x_ray_analyzer')
def x_ray_analyzer():
    return render_template('x_ray_analyzer.html')

@app.route('/ecg_analyzer')
def ecg_analyzer():
    return render_template('ecg_analyzer.html')

@app.route("/blood_report_analyzer", methods=["GET", "POST"])
def blood_report_analyzer():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file:
            # Add file handling logic here (e.g., save or analyze file)
            return "File uploaded successfully!"
    return render_template("blood_report_analyzer.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
