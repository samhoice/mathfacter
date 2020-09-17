from invoke import task


@task
def docker_manage(c, cmd):
    c.run("docker-compose run web python3 manage.py {}".format(cmd), pty=True)
