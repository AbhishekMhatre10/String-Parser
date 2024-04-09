from flask import Flask, request, jsonify,render_template
from parser.parser_1 import parse_text
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    sentence = data['sentence']
    result = parse_text(sentence)
    # Use json.loads to convert the JSON string returned by parse_text into a Python dict
    result_dict = json.loads(result)
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(debug=True)
