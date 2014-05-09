from fabric.api import local

def create_local_db(db_name='beerfinder'):
    local("createdb -T template_postgis {0}".format(db_name))
