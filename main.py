from app import create_app, db
from app.models import User
from sqlalchemy import exc


app = create_app()
with app.test_request_context():
    db.create_all()
    try:
        if not User.query.filter_by(user_name='raai').first():
            User.create_user(user_name='raai', user_email='raai@gmail.com', user_password='secret', user_phone_num='9903020341')
    except exc.IntegrityError:
        app.run(debug=True)

