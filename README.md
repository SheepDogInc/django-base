## Using this template

To create a new project with this template, run the following command:

    bash <(curl -fsSL https://raw.github.com/SheepDogInc/django-base/master/new_project.sh)

This section can be removed once you are done.

----------------------------------------------------------------------

# {{ project_name }}

## Getting Bootstrapped

### Automatically

Run `./setup.sh`.

### Manually

Clone & create virtual env:

    git clone git@github.com:SheepDogInc/{{ project_name }}.git {{ project_name }}
    cd {{ project_name }}/
    mkvirtualenv {{ project_name }}

Install Python & Node dependencies:

    pip install -r requirements.txt
    npm install

Add local Node modules to your `$PATH` in virtualenv's `postactivate` script:

    printf 'export PATH=%s/node_modules/.bin:$PATH\n' `pwd` >> $VIRTUAL_ENV/bin/postactivate
    workon {{ project_name }}

Install CSS & JS dependencies:

    bower install

Finish up:

    ./manage.py syncdb
    ./manage.py migrate

### Heroku-specific stuff

For heroku deployments, use a buildback which knows about combining node and
python.  Otherwise, Heroku will auto-detect one w/o the other and
requirements will not be installed.

    heroku config:set BUILDPACK_URL='https://github.com/thurloat/heroku-buildpack-python.git'
    heroku addons:add heroku-postgresql:dev

While we are on the topic of heroku keys, you might as well set other
environment variables as needed:

    AWS_ACCESS_KEY_ID          # use a project-specific one!!
    AWS_SECRET_ACCESS_KEY
    ENV                        # the environment you're deploying ie: dev/prod
