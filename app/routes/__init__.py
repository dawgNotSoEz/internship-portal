from flask import Blueprint, jsonify

# Import all route modules
from app.routes.api.auth import auth_routes
from app.routes.api.admin import admin_routes, analytics_routes
from app.routes.api.company import company_routes
from app.routes.api.search import search_routes

# Create main API blueprint
api_bp = Blueprint('api', __name__)

# Register all route blueprints
try:
    api_bp.register_blueprint(auth_routes.auth_bp, url_prefix='/auth')
except AttributeError:
    print("Warning: auth_bp not found in auth_routes")

try:
    api_bp.register_blueprint(admin_routes.admin_bp, url_prefix='/admin')
except AttributeError:
    print("Warning: admin_bp not found in admin_routes")

try:
    api_bp.register_blueprint(analytics_routes.analytics_bp, url_prefix='/admin/analytics')
except AttributeError:
    print("Warning: analytics_bp not found in analytics_routes")

try:
    api_bp.register_blueprint(company_routes.company_bp, url_prefix='/company')
except AttributeError:
    print("Warning: company_bp not found in company_routes")

try:
    api_bp.register_blueprint(search_routes.search_bp, url_prefix='/search')
except AttributeError:
    print("Warning: search_bp not found in search_routes")

# Debug route
@api_bp.route('/debug', methods=['GET'])
def debug():
    """Debug route to check database connection and collections."""
    from app import db, mongo
    
    try:
        # Test MongoDB connection
        mongo.admin.command('ping')
        
        # Get basic debug info
        debug_info = {
            'database_name': db.name,
            'collections': db.list_collection_names(),
            'students_count': db.students.count_documents({})
        }
        
        return jsonify({
            'status': 'success',
            'debug_info': debug_info
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Firebase test route
@api_bp.route('/firebase-test', methods=['GET'])
def firebase_test():
    """Test route to verify Firebase connection."""
    from app.utils.firebase_setup import initialize_firebase, push_test_message
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Firebase test endpoint called")
        # Initialize Firebase
        firebase_initialized = initialize_firebase()
        
        if not firebase_initialized:
            logger.error("Firebase initialization failed")
            return jsonify({
                'status': 'error',
                'message': 'Firebase initialization failed'
            }), 500
        
        # Push test message
        message_sent = push_test_message()
        
        if message_sent:
            logger.info("Firebase test message sent successfully")
            return jsonify({
                'status': 'success',
                'message': 'Firebase test message sent successfully'
            }), 200
        else:
            logger.error("Failed to send Firebase test message")
            return jsonify({
                'status': 'error',
                'message': 'Failed to send Firebase test message'
            }), 500
    
    except Exception as e:
        logger.exception(f"Error in Firebase test endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Dummy data population route
@api_bp.route('/populate-dummy-data', methods=['POST'])
def populate_dummy_data_route():
    """Route to populate the database with dummy data for testing."""
    from app.utils.dummy_data import populate_dummy_data
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("Populate dummy data endpoint called")
    
    try:
        # Populate dummy data
        summary = populate_dummy_data()
        
        logger.info(f"Dummy data populated successfully: {summary}")
        return jsonify({
            'status': 'success',
            'message': 'Dummy data populated successfully',
            'summary': summary
        }), 200
    
    except Exception as e:
        logger.exception(f"Error populating dummy data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
