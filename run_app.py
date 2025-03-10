import os
import sys
import time
import subprocess
from pyngrok import ngrok
from loguru import logger

# Setup logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    colorize=True,
)

def run_with_ngrok(port=8501):
    """Run the Streamlit app with ngrok tunnel."""
    try:
        # Get ngrok auth token from environment variable or prompt user
        ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN")
        if not ngrok_auth_token:
            ngrok_auth_token = input("Enter your ngrok auth token: ")
            
        # Set ngrok auth token
        logger.info("Setting up ngrok tunnel...")
        ngrok.set_auth_token(ngrok_auth_token)
        
        # Start ngrok tunnel to the streamlit port
        public_url = ngrok.connect(port).public_url
        logger.success(f"Ngrok tunnel established! Access your app at: {public_url}")
        logger.info("Share this URL with your friend to access the app")
        logger.warning("Note: The URL will change if you restart the application")
        
        # Run the streamlit app
        logger.info(f"Starting Streamlit server on port {port}...")
        subprocess.run([
            "streamlit", "run", 
            "app.py", 
            "--server.port", str(port),
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
        ])
    except Exception as e:
        logger.error(f"Error setting up ngrok tunnel: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up ngrok tunnel
        ngrok.kill()

if __name__ == "__main__":
    # Run the app with ngrok
    run_with_ngrok()