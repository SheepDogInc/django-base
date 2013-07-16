#!/bin/bash

PROJECT={{ project_name }}

function echo_exit {
    echo ABORTING: $*
    exit 1
}

# Make sure we are in the root directory where the setup executable lives
if [ "`echo $0 | cut -c1`" = "/" ]; then
  cd `dirname $0`
else
  cd `pwd`/`echo $0 | sed -e s/setup//`
fi

## Check for required executables
for ex in python2.7 virtualenv virtualenvwrapper.sh
do
    command -v $ex >/dev/null 2>&1 || { echo >&2 echo_exit "Executable '$ex' is required but not installed.  Aborting."; }
done

# Check for normal files we expect
for f in manage.py requirements.txt $PROJECT/settings/base.py
do
  if [ ! -e $f ]
  then echo_exit "File $f not found"
  fi
done

# Check if we already ran the setup script:
for f in $PROJECT/static/bower $WORKON_HOME/$PROJECT
do
  if [ -e $f ]
  then
    echo "File $f already exists; perhaps you already ran the setup?"
    echo "To try again, run the following first: "
    echo "   rm -rf $PROJECT ; rmvirtualenv $PROJECT ; git reset HEAD ; git checkout . "
    exit 1;
  fi
done

# Install all dependencies
source `which virtualenvwrapper.sh`
mkdir -p $PROJECT/static/js
mkvirtualenv --python=python2.7 --no-site-packages $PROJECT
pip install -r requirements.txt
npm install
printf 'export PATH=%s/node_modules/.bin:$PATH\n' `pwd` >> $VIRTUAL_ENV/bin/postactivate
workon $PROJECT
bower install

echo "============================"
echo "TO PROCEED:"
echo "(1) => Create database $PROJECT"
echo "(2) ./manage.py syncdb"
echo "(3) ./manage.py migrate"