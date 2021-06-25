import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def query(sqlcmd):
    conn = get_db()

    conn.row_factory = dict_factory

    cursor = conn.cursor()

    cursor.execute(sqlcmd)
    result = cursor.fetchone()
    
    cursor.close()
    return result

def execution(sqlcmd):
    conn = get_db()
    cursor = conn.execute(sqlcmd)
    conn.commit()
    select = "select * from userProfile where id={}".format(cursor.lastrowid)
    result = query(select)
    cursor.close()
    return result

def dict_factory(cursor,row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d