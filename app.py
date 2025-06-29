# Flask API for Google Shopping Scraper
# POST /scrape expects a JSON body with keys like:
# {
#     "top_wear_search_engine_query": "normal fitting shirts for men",
#     "bottom_wear_search_engine_query": "pants for men",
#     "shoes_search_engine_query": "sports sneaker for men",
#     "color_recommendations_search_engine_query": "sky tone colors for men"
# }

from flask import Flask, request, jsonify
from docker_scraper import run_scraper

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    params = request.json  # Should match the above structure
    try:
        results = run_scraper(params)
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 