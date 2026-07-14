import os
import sys
import click
from pathlib import Path



from dotenv import load_dotenv

load_dotenv()


COV = None
if os.getenv('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db   # noqa: E402
from app.models import Role, User # noqa: E402

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)



@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """ Run the unit tests. """
    if coverage and not os.getenv('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary: ')
        COV.report()
        basedir = Path(__file__).parent.resolve()
        covdir = basedir / 'tmp/coverage'
        COV.html_report(directory=str(covdir))
        print(f'HTML version: file://{covdir}/index.html')
        COV.erase()

@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')

def profile(length, profile_dir):
    """ Start the application under the code profiler. """
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    os.environ.pop('FLASK_RUN_FROM_CLI', None)
    app.run(debug=False)
