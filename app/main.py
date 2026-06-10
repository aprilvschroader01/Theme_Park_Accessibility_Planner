"""
Main Flask Application for Theme Park Accessibility Planner
"""
from flask import Flask, render_template, request, jsonify
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from config import DEBUG
from database import init_database, save_query, save_result, get_query_results
from agents.dietary_agent import create_dietary_agent

app = Flask(__name__)
app.config['DEBUG'] = DEBUG

# Initialize database on startup
with app.app_context():
    init_database()

@app.route('/')
def index():
    """Home page with query form"""
    return render_template('index.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """
    Generate a dietary plan for the user's query
    Expects JSON with: park_name, dietary_restrictions, allergens
    """
    try:
        data = request.json
        park_name = data.get('park_name', '').strip()
        dietary_restrictions = [r.strip() for r in data.get('dietary_restrictions', '').split(',') if r.strip()]
        allergens = [a.strip() for a in data.get('allergens', '').split(',') if a.strip()]
        
        if not park_name:
            return jsonify({"error": "Park name is required"}), 400
        
        # Save the query
        query_text = f"Dietary plan for {park_name}"
        query_id = save_query(
            park_name=park_name,
            query_text=query_text,
            dietary_restrictions=', '.join(dietary_restrictions),
            allergens=', '.join(allergens)
        )
        
        # Generate the plan using the dietary agent
        agent = create_dietary_agent()
        result = agent.generate_plan(
            park_name=park_name,
            dietary_restrictions=dietary_restrictions,
            allergens=allergens
        )
        
        if not result['success']:
            return jsonify({
                "error": f"Failed to generate plan: {result.get('error', 'Unknown error')}"
            }), 500
        
        # Save the result
        save_result(
            query_id=query_id,
            park_section="Full Plan",
            restaurant_name="All",
            menu_items="",
            dietary_notes="",
            result_json=result['plan']
        )
        
        return jsonify({
            "success": True,
            "query_id": query_id,
            "park": park_name,
            "plan": result['plan'],
            "dietary_restrictions": dietary_restrictions,
            "allergens": allergens
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/query/<int:query_id>', methods=['GET'])
def get_plan(query_id):
    """Retrieve a previously generated plan"""
    try:
        results = get_query_results(query_id)
        if not results:
            return jsonify({"error": "Query not found"}), 404
        
        # Extract the plan from the first result (contains full plan)
        plan_json = results[0]['result_json'] if results else None
        
        return jsonify({
            "success": True,
            "query_id": query_id,
            "plan": plan_json
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/results/<int:query_id>')
def results_page(query_id):
    """Display results for a specific query"""
    return render_template('results.html', query_id=query_id)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
