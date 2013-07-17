#!/bin/bash

# Only use this script if you are bootstrapping a new project. Once a project
# is bootstrapped, use setup.sh.

read -p "Project name for env and main project dir (django_base)? " PROJECT
if [ -z "$PROJECT" ]; then
    PROJECT=django_base
fi

function echo_exit {
    echo ABORTING: $*
    exit 1
}

# Check for required executables
for ex in python2.7 virtualenv virtualenvwrapper.sh
do
    command -v $ex >/dev/null 2>&1 || { echo >&2 echo_exit "Executable '$ex' is required but not installed. Aborting."; }
done

# Create virtualenv with just Django
source `which virtualenvwrapper.sh`
mkvirtualenv --python=python2.7 --no-site-packages $PROJECT
pip install Django==1.6b1 --find-links https://s3.amazonaws.com/sheepdog-assets/feta/index.html

# Create project based on django-base template
django-admin.py startproject --template=https://github.com/SheepDogInc/django-base/archive/project-template.zip --extension=py,json,md,sh,bowerrc --name=Procfile $PROJECT
cd $PROJECT
rm new_project.sh
chmod +x setup.sh

echo "============================"
echo "TO PROCEED:"
echo "(1) cd $PROJECT"
echo "(2) ./setup.sh"
