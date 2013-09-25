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

### Common problems

- Make sure there is no dynamic content inside compress tags.


### Heroku-specific stuff

For heroku deployments, use a buildback which knows about combining node and
python.  Otherwise, Heroku will auto-detect one w/o the other and
requirements will not be installed.

    heroku config:set BUILDPACK_URL='https://github.com/heroku/heroku-buildpack-python' # Node not needed
    heroku config:set BUILDPACK_URL='https://github.com/thurloat/heroku-buildpack-python.git' # Node needed

    heroku addons:add heroku-postgresql:dev

Set up an S3 root bucket (for the project, not for each deployment).
Confirm the bucket name matches that in settings/heroku/base.py.  Add
an IAM user for each deployment, and give it copy an appropriate
permissions from another project.  Last, set the heroku config
variables:

    AWS_ACCESS_KEY_ID          # use a project-specific one!!
    AWS_SECRET_ACCESS_KEY
    SECRET_KEY                 # Django secret key

Confirm the following is set:

    DATABASE_URL
