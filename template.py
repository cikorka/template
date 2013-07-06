#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

GIT = '{}/vendors'.format(os.getcwd())  # vendors repositories directory

REPOS = {
    'bootstrap': 'git://github.com/twitter/bootstrap.git',
    'boilerplate': 'git://github.com/h5bp/html5-boilerplate.git',
    'font-awesome': 'git://github.com/FortAwesome/Font-Awesome.git',
    'retinajs': 'git://github.com/imulus/retinajs.git',
}

try:
    STATIC = sys.argv[1]  # static files root directory
except IndexError:
    STATIC = '%s/static' % os.getcwd()  # static files root directory


def make():
    """
    Main method

    Update cloned repositories and copy less and js files
    info {STATIC} directory  and then compile less to css files in {STATIC}/css

    """

    get_vendors()  # clone or pull vendors directory

    # delete previous template
    if os.access(STATIC, os.R_OK):
        shutil.rmtree(STATIC)

    # copy LESS files
    ## copy bootstrap LESS files
    shutil.copytree('%s/bootstrap/less' % GIT, '%s/less/bootstrap' % STATIC)
    ## copy font awesome LESS files
    shutil.copytree('%s/font-awesome/less' % GIT, '%s/less/font-awesome' % STATIC)
    ## copy font retinajs LESS files
    os.mkdir('%s/less/retina' % STATIC)
    shutil.copy('%s/retinajs/src/retina.less' % GIT, '%s/less/retina/retina.less' % STATIC)

    # copy JS files
    ## copy font boilerplate JS files
    shutil.copytree('%s/boilerplate/js' % GIT, '%s/js' % STATIC)
    ## copy bootstrap JS files
    shutil.copytree('%s/bootstrap/js' % GIT, '%s/js/vendor/bootstrap' % STATIC)
    ## copy font retinajs JS files
    shutil.copy('%s/retinajs/src/retina.js' % GIT, '%s/js/vendor/retina.js' % STATIC)

    # copy FONT files
    shutil.copytree('%s/font-awesome/font' % GIT, '%s/font' % STATIC)

    # copy boilerplate root files
    for copied_file in ['index.html', 'robots.txt', 'crossdomain.xml']:
        shutil.copy('%s/boilerplate/%s' % (GIT, copied_file), '%s/%s' % (STATIC, copied_file))

    _lessc()  # compile LESS files

    print 'Done. Saved into', STATIC


def _lessc():
    os.mkdir('{}/css'.format(STATIC))  # create CSS directory in STATIC root

    # create and write file main.less
    # and write into this files importing statements of vendors less files
    f = file('{}/less/main.less'.format(STATIC), 'w')
    f.write('//\n// Root LESS file\n//\n\n')
    f.write('@import "./retina/retina.less";\n')
    f.write('@import "./bootstrap/bootstrap.less";\n')
    f.write('@import "./font-awesome/font-awesome.less";\n')
    f.close()

    # compile less file into css directory
    os.system('/usr/local/bin/lessc {0}/less/main.less > {0}/css/main.css'.format(STATIC))

    # compress copiled file and remove new lines
    os.system('/usr/local/bin/lessc {0}/css/main.css --compress > {0}/css/main.min.css'.format(STATIC))
    f = file('{}/css/main.min.css'.format(STATIC), 'r')
    content = f.read()
    f.close()
    f = file('{}/css/main.min.css'.format(STATIC), 'w')
    f.write(content.replace('\n', ' '))
    f.close()


def get_vendors():
    # check if git directory exist
    # if exist pull otherwise clone git repos
    if not os.access(GIT, os.R_OK):
        os.mkdir(GIT)  # create directory for git repositories

    for key, value in REPOS.iteritems():
        if os.access('%s/%s' % (GIT, key), os.R_OK):
            print 'Repository %s/%s' % (GIT, key)
            # pull git repository
            os.system('cd %s && cd %s && git pull' % (GIT, key))
        else:
            # clone git repository
            os.system('cd %s && git clone %s %s' % (GIT, value, key))


if __name__ == '__main__':
    make()
