import functools
import json
import click
from erp import db
from flask import current_app, g
from flask.cli import with_appcontext

def init_generator(app):
    app.cli.add_command(do_generate_create_html)

@click.group()
def cli():
    pass

@click.command('gen_html')
@click.argument('name')
@with_appcontext
def do_generate_create_html(name):
    print('Generate db {name}'.format(name = name))
    
    #with open('create_outer.html','r') as outerfile:
    #    with open('create_inner.html', 'r') as innerfile:
    #        print("generate")
#@click.option('--count', default=1, help='number of greetings')
#@click.argument('name')

