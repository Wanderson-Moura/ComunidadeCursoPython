from comunidade import app, database
# from comunidade.models import Usuario
#
#
with app.app_context():
    database.drop_all()
    database.create_all()
# with app.app_context():
#     usuario = Usuario(username="wanderson", senha="123456", email="wand@gmail.com")
#     database.session.add(usuario)
#     database.session.commit()
# with app.app_context():
#     Usuario.query.all()
