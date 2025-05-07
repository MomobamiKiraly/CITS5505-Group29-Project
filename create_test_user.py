from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()


if not User.query.filter_by(username='testuser').first():
    user = User(username='testuser', email='test@example.com')
    user.set_password('test123') 
    db.session.add(user)
    db.session.commit()
    print("✅ Test user created: testuser / test123")
else:
    print("ℹ️ User 'testuser' already exists.")