from django import test
from django.db import connection
from django.core.management import call_command
from core.models import Sport
from io import StringIO
import warnings
import sys
import traceback

from data_importer.FFTri import FFTri

test.utils.setup_test_environment()
db = connection.creation.create_test_db()

try:
    call_command('loaddata', 'core/fixtures/sports.yaml', format='yaml', verbosity=1)


    data = FFTri()
    data.import_events_in_app('Duathlon', geocode=False, limit=10)


    # Export to fixture
    buf = StringIO()
    call_command('dumpdata','core', format='yaml', stdout=buf)
    buf.seek(0)
    with open('data_importer/FFTri_out.yaml', 'w') as f:
        f.write(buf.read())

except Exception as e:
    print('Something went wrong...')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print (''.join('!! ' + line for line in lines))

finally:
    connection.creation.destroy_test_db(db)
    test.utils.teardown_test_environment()