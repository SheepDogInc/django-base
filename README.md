# Sheepdog Django Skeleton

## Getting Bootstrapped

### Automatically

Run `./setup`.

### Manually

Clone & create virtual env:

    git clone git@github.com:SheepDogInc/django-base.git myproject
    cd myproject/
    mkvirtualenv myproject

Install Python & Node dependencies:

    pip install -r requirements.txt -f https://s3.amazonaws.com/sheepdog-assets/feta/index.html --no-index
    npm install

Add local Node modules to your `$PATH` in virtualenv's `postactivate` script:

    printf 'export PATH=%s/node_modules/.bin:$PATH\n' `pwd` >> $VIRTUAL_ENV/bin/postactivate
    workon myproject

Install CSS & JS dependencies:

    bower install

Finish up:

    ./manage.py syncdb
    ./manage.py migrate
