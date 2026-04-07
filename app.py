from flask import Flask, request, jsonify
from services import Location   # your file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/irradiation', methods=['GET'])
def get_irradiation():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    # Create object
    loc = Location(float(lat), float(lon))

    # Call your methods
    max_year, max_irradiation = loc.max_irradiance_and_year()
    min_year, min_irrad = loc.min_irradiance_and_year()
    avg_irrad = loc.avg_irradiance()

    return jsonify({
        "max_year": max_year,
        "max_irradiation": max_irradiation,
        "min_year": min_year,
        "min_irradiation": min_irrad,
        "avg_irradiation": avg_irrad
    })

if __name__ == '__main__':
    app.run(debug=True)