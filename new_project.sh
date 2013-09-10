#!/bin/bash

# Only use this script if you are bootstrapping a new project. Once a project
# is bootstrapped, use setup.sh.

TEMPLATE=https://github.com/SheepDogInc/django-base/archive/master.zip

function echo_exit {
    echo ABORTING: $*
    exit 1
}

if [ -n "$VIRTUAL_ENV" ]; then
    echo_exit "Deactivate your virtualenv by typing 'deactivate' and run this script again."
fi

if [[ $# == 0 ]]; then
    read -p "Project name for env and main project dir (django_base)? " PROJECT
elif [[ $# == 1 ]]; then
    PROJECT=$1
elif [[ $# == 2 ]]; then
    PROJECT=$1
    TEMPLATE=$2
else
    echo "Usage:"
    echo
    echo "  new_project.sh"
    echo "  new_project.sh PROJECT_NAME"
    echo "  new_project.sh PROJECT_NAME DJANGO_PROJECT_TEMPLATE"
    echo
    exit 1
fi

if [[ ! "$PROJECT" =~ ^[a-zA-Z_0-9]+$ ]] ; then
    echo_exit "Project name must consist of underscore, letters, and digits"
fi

# Check for required executables
for ex in python2.7 virtualenv virtualenvwrapper.sh
do
    command -v $ex >/dev/null 2>&1 || { echo >&2 echo_exit "Executable '$ex' is required but not installed."; }
done

# Create virtualenv with just Django
source `which virtualenvwrapper.sh`
mkvirtualenv --python=python2.7 --no-site-packages $PROJECT
pip install Django==1.6b2 --find-links https://s3.amazonaws.com/sheepdog-assets/feta/index.html

# Create project based on django-base template
django-admin.py startproject --template=$TEMPLATE --extension=py,json,md,sh,bowerrc --name=Procfile $PROJECT
cd $PROJECT
rm new_project.sh
chmod +x setup.sh manage.py

echo "============================"
echo "TO PROCEED:"
echo "(1) cd $PROJECT"
echo "(2) ./setup.sh"
