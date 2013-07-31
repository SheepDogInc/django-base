#!/bin/bash

# Only use this script if you are bootstrapping a new project. Once a project
# is bootstrapped, use setup.sh.


function echo_exit {
    echo ABORTING: $*
    exit 1
}

if [ -n "$VIRTUALENV" ]; then
    echo_exit "Deactivate your virtualenv by typing 'deactivate' and run this script again."
fi

read -p "Project name for env and main project dir (django_base)? " PROJECT
if [ -z "$PROJECT" ]; then
    PROJECT=django_base
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
pip install Django==1.6b1 --find-links https://s3.amazonaws.com/sheepdog-assets/feta/index.html

# Create project based on django-base template
django-admin.py startproject --template=https://github.com/SheepDogInc/django-base/archive/master.zip --extension=py,json,md,sh,bowerrc --name=Procfile $PROJECT
cd $PROJECT
rm new_project.sh
chmod +x setup.sh

echo "============================"
echo "TO PROCEED:"
echo "(1) cd $PROJECT"
echo "(2) ./setup.sh"
