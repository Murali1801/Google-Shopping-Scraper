from flask import Flask, request, jsonify
from docker_scraper import GoogleShoppingScraper

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        input_data = request.get_json(force=True)
        scraper = GoogleShoppingScraper()
        result = scraper.run_scraper_from_dict(input_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 