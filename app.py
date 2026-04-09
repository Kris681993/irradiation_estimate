from flask import Flask, request, jsonify
from services import Location, Site_details   # your file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/evaluate-generation', methods=['GET'])
def get_data():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    pr = request.args.get('pr')

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    # Create object
    loc = Location(float(lat), float(lon))
    site_details = Site_details(loc, (float(pr)/100))

    # Call your methods
    max_year, max_irradiation = loc.max_irradiance_and_year()
    min_year, min_irrad = loc.min_irradiance_and_year()
    avg_irrad = loc.avg_irradiance()
    max_gen = site_details.max_generation()
    min_gen = site_details.min_generation()
    avg_gen = site_details.avg_generation()

    return jsonify({
        "max_year": max_year,
        "max_irradiation": max_irradiation,
        "min_year": min_year,
        "min_irradiation": min_irrad,
        "avg_irradiation": avg_irrad,
        'max_generation' : max_gen,
        'min_generation' : min_gen,
        'avg_generation' : avg_gen
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# git init
# git add .
# git commit -m "initial commit"
# git branch -M main
# git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
# git push -u origin main