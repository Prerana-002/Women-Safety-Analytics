from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reports.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

@app.route("/")
def home():
    reports = Report.query.all()
    return render_template("index.html", reports=reports)

@app.route("/report", methods=["POST"])
def report():
    location = request.form["location"]
    description = request.form["description"]
    lat, lng = get_coordinates(location)  # Function to fetch lat/lng from location
    new_report = Report(location=location, description=description, lat=lat, lng=lng)
    db.session.add(new_report)
    db.session.commit()
    return redirect("/")

def get_coordinates(location):
    # Dummy lat/lng, replace with API call to get real coordinates
    return (20.5937, 78.9629)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
