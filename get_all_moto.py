from webapp import create_app
from webapp.motorcycles.parsers import avito

app = create_app()
with app.app_context():
    avito.get_moto_content()
