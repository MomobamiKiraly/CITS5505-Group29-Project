from app.forms import RegisterForm

def test_register_form_fields(app):  # 接收 app fixture
    with app.app_context():
        form = RegisterForm()
        assert hasattr(form, 'username')
        assert hasattr(form, 'email')
        assert hasattr(form, 'password')