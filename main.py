from flask import Flask, jsonify
from los import line_of_sight

app = Flask(__name__)

@app.route('/')
def lineofsight():
    # Example coordinates (Jerusalem approx)
    start = [31.7719, 35.2170]
    end = [31.8, 35.25] 
    result = line_of_sight(start, end)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
