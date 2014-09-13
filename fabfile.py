from fabric.api import local

def create_local_db(db_name='beerfinder'):
    local("createdb -T template_postgis {0}".format(db_name))

def save_git_sha1():
    local('''echo "REQUIRE_BUILD_PATH=\\""`git rev-parse HEAD`"\\"" > beerfinder/beerfinder/settings/git_head.py''')

def deploy_local():
    """
    Deploy to be called locally after a git fetch.  Be sure to be in the virtualenv.
    """

    save_git_sha1()
    local("python ./beerfinder/manage.py syncdb")
    local("python ./beerfinder/manage.py migrate")
    local("python ./beerfinder/manage.py collectstatic")


