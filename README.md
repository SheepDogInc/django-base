## Using this template

To create a new project with this template, run the following command:

    bash <(curl -fsSL https://raw.github.com/SheepDogInc/django-base/project-template/new_project.sh)

----------------------------------------------------------------------

# {{ project_name }}

## Getting Bootstrapped

### Automatically

Run `./setup.sh`.

### Manually

Clone & create virtual env:

    git clone git@github.com:SheepDogInc/{{ project_name }}.git myproject
    cd myproject/
    mkvirtualenv myproject

Install Python & Node dependencies:

    pip install
    npm install

Add local Node modules to your `$PATH` in virtualenv's `postactivate` script:

    printf 'export PATH=%s/node_modules/.bin:$PATH\n' `pwd` >> $VIRTUAL_ENV/bin/postactivate
    workon myproject

Install CSS & JS dependencies:

    bower install

Finish up:

    ./manage.py syncdb
    ./manage.py migrate
