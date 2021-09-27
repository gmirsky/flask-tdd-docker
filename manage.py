# manage.py


import sys

from flask.cli import FlaskGroup

from src import create_app, db
from src.api.users.models import User


app = create_app()  
cli = FlaskGroup(create_app=create_app)  # new


@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='old_devil', email="old_devil@vanapagan.com"))
    db.session.add(User(username='seven_twelfths', email="seven_twelfths@septunx.com"))
    db.session.add(User(username='ima.dummy', email="ima.dummy@fakedomain.com"))
    db.session.add(User(username='go_away', email="go_away@noreply.com"))
    db.session.add(User(username='pebcak', email="pebcak@braindeadusers.com"))
    db.session.commit()


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
