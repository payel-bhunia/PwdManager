from app import create_app, db
from app.models import User
from sqlalchemy import exc
from werkzeug.security import generate_password_hash

app = create_app()
with app.test_request_context():
    db.create_all()
    try:
        if not User.query.filter_by(user_name='raai').first():
            new_user = User(user_email='raai@gmail.com', user_name='raai', user_password=generate_password_hash(
                    'secret', method='sha256'))
            db.session.add(new_user)
            db.session.commit()
    except exc.IntegrityError:
        app.run(debug=True)

