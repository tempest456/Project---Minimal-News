from app.email import distribute_news
from app.engine import news_spider
from app.models import News, User, categories
from app import create_app, db
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, News=News, User=User, categories=categories)


@app.cli.command()
def test():
    """ Run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def scrape():
    """ Run the scraper """
    news_spider.run_spider()


@app.cli.command()
def distribute():
    """ Distribute the newsletter """
    batch = {0: 'morning', 6: 'noon', 12: 'evening'}
    users = User.query.filter_by(confirmed=True,
                                 preferred_time=batch.get(datetime.utcnow().hour))
    news_obj = News.query.limit(12)
    try:
        corona_stat = requests.get(
                'https://nepalcorona.info/api/v1/data/nepal/').json()
    except:
        pass
    distribute_news(users, 'newsletter', news_obj=news_obj, corona_stat=corona_stat)


@app.cli.command()
def deploy():
    """ Run deployment tasks """
    db.create_all()

