from app.forms import RegisterForm

# Test to check if RegisterForm contains required fields
def test_register_form_fields(app):  # Receives the app fixture
    with app.app_context():
        form = RegisterForm()
        assert hasattr(form, 'username')  # Check if form has 'username' field
        assert hasattr(form, 'email')     # Check if form has 'email' field
        assert hasattr(form, 'password')  # Check if form has 'password' field