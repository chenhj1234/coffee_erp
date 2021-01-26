import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    #@app.route('/')
    #def hello():
    #    return 'Hello, World!'

    from . import db
    with app.app_context():
        db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import rawbean
    app.register_blueprint(rawbean.bp)

    from . import supplier
    app.register_blueprint(supplier.bp)

    from . import customer
    app.register_blueprint(customer.bp)

    from . import purchase
    app.register_blueprint(purchase.bp)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from . import generate_template
    generate_template.init_generator(app)
    
    return app

