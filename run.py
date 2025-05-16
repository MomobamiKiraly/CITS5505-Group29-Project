from app import create_app

# Create the Flask application instance using the factory function
app = create_app()

# Run the Flask development server if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)

