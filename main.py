from app import create_app, db


app = create_app()
with app.test_request_context():
    db.create_all()
app.run(debug=True)

