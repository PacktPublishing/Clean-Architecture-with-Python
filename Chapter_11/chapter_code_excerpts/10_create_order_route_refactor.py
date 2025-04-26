# Modified route in order_system/app.py
from flask import request, jsonify

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Basic input validation remains in the route handler
    if not data or not 'customer_id' in data or not 'items' in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Feature flag to control which implementation handles the request
        if app.config.get('USE_CLEAN_ARCHITECTURE', False):
            # Use the clean implementation
            result = order_controller.handle_create_order(data)
            return jsonify(result), 201
        else:
            # ... original implementation remains here ...
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except SystemError:
        return jsonify({'error': 'Internal server error'}), 500