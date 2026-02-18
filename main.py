from flask import Flask, jsonify, request
from flask_cors import CORS
from los import line_of_sight, isVisible

app = Flask(__name__)
CORS(app)

@app.route('/')
def lineofsight():
    s_lat = request.args.get('start_lat', type=float)
    s_lng = request.args.get('start_lng', type=float)
    e_lat = request.args.get('end_lat', type=float)
    e_lng = request.args.get('end_lng', type=float)
    
    if None in [s_lat, s_lng, e_lat, e_lng]:
        return jsonify({"error": "Missing coordinates. Requires start_lat, start_lng, end_lat, end_lng"}), 400

    start = [s_lat, s_lng]
    end = [e_lat, e_lng] 
    los = line_of_sight(start, end)
    result = isVisible(los[3], los[1])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
