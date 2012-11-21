from fabric.colors import red
from fabric.operations import local
import os
import sys

APPS = []
TESTS = [' '.join(APPS)]
COVERAGE_SOURCES = ','.join(APPS)
COVERAGE_PARAMS = "--omit='*migrations*,*tests*"

def test():
    """
    Run unit tests for this Django Application
    """
    if len(APPS) == 0:
        return
    local('python manage.py test %s' % TESTS)


def coverage():
    """
    Generate Coverage report for this Django Application
    """
    if len(APPS) == 0:
        return
    local('coverage run --source=%s ./manage.py test %s' % COVERAGE_SOURCES, TESTS)
    print '============================================'
    print 'Coverage Results:'
    local('coverage report %s' % COVERAGE_PARAMS)
    local('rm .coverage')

try:
    assert os.getcwd() == os.path.dirname(os.path.abspath(__file__))
except AssertionError:
    print red("You're doing it wrong dude. Run this from the root.")
    sys.exit(1)