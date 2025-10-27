"""Flask app factory for DexPhish placeholder project."""
from flask import Flask, render_template
import os
import logging


def configure_logging():
    """Set up logging for the application."""
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


def validate_directories(logger, template_dir, static_dir):
    """Ensure required directories exist."""
    if not os.path.exists(template_dir):
        logger.error(f"Template directory not found: {template_dir}")
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    if not os.path.exists(static_dir):
        logger.error(f"Static directory not found: {static_dir}")
        raise FileNotFoundError(f"Static directory not found: {static_dir}")


def create_app():
    """Create and configure the Flask application."""
    logger = configure_logging()

    try:
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

        validate_directories(logger, template_dir, static_dir)

        app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

        # Register routes
        @app.route('/')
        def index():
            try:
                return render_template('dashboard.html')
            except Exception as e:
                logger.error(f"Error rendering 'dashboard.html': {e}")
                return "An error occurred while loading the dashboard.", 500

        @app.route('/campaign')
        def campaign():
            try:
                return render_template('campaign.html')
            except Exception as e:
                logger.error(f"Error rendering 'campaign.html': {e}")
                return "An error occurred while loading the campaign page.", 500

        return app
    except Exception as e:
        logger.error(f"Error initializing Flask app: {e}")
        raise

# Ensure Flask is installed
try:
    import flask
except ImportError:
    import pip
    pip.main(['install', 'flask'])
