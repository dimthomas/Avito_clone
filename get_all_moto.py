from webapp import create_app
from webapp.avito import get_page_data, get_html, get_all_url

app = create_app()
with app.app_context():
    get_page_data(get_html(get_all_url()))