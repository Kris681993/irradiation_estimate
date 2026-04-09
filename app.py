from flask import Flask, request, jsonify
from flask_cors import CORS
from services import Location, Site_details
import os

app = Flask(__name__)
CORS(app)


@app.route("/evaluate-generation", methods=["GET"])
def get_data():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        pr = request.args.get("pr")
        cap = request.args.get("plant-capacity")

        missing_params = []
        if lat is None or lat == "":
            missing_params.append("lat")
        if lon is None or lon == "":
            missing_params.append("lon")
        if pr is None or pr == "":
            missing_params.append("pr")
        if cap is None or cap == "":
            missing_params.append("plant-capacity")

        if missing_params:
            return jsonify({
                "error": f"Missing required query parameter(s): {', '.join(missing_params)}"
            }), 400

        try:
            lat = float(lat)
            lon = float(lon)
            pr = float(pr)
            cap = float(cap)
        except ValueError:
            return jsonify({
                "error": "lat, lon, pr, and plant-capacity must be valid numbers"
            }), 400

        if not (-90 <= lat <= 90):
            return jsonify({"error": "Latitude must be between -90 and 90"}), 400

        if not (-180 <= lon <= 180):
            return jsonify({"error": "Longitude must be between -180 and 180"}), 400

        if pr < 0:
            return jsonify({"error": "pr must be greater than or equal to 0"}), 400

        if cap < 0:
            return jsonify({"error": "plant-capacity must be greater than or equal to 0"}), 400

        loc = Location(lat, lon)
        site_details = Site_details(loc, pr, cap)

        max_year, max_irradiation = loc.max_irradiance_and_year()
        min_year, min_irrad = loc.min_irradiance_and_year()
        avg_irrad = loc.avg_irradiance()

        max_gen = site_details.max_generation()
        min_gen = site_details.min_generation()
        avg_gen = site_details.avg_generation()

        max_plant_gen = site_details.max_plant_generation()
        min_plant_gen = site_details.min_plant_generation()
        avg_plant_gen = site_details.avg_plant_generation()

        return jsonify({
            "max_year": int(max_year),
            "max_irradiation": round(float(max_irradiation), 2),
            "min_year": int(min_year),
            "min_irradiation": round(float(min_irrad), 2),
            "avg_irradiation": round(float(avg_irrad), 2),
            "max_generation": round(float(max_gen), 2),
            "min_generation": round(float(min_gen), 2),
            "avg_generation": round(float(avg_gen), 2),
            "max_plant_gen": round(float(max_plant_gen), 2),
            "min_plant_gen": round(float(min_plant_gen), 2),
            "avg_plant_gen": round(float(avg_plant_gen), 2)
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Irradiation Estimate API is running",
        "endpoint": "/evaluate-generation"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )