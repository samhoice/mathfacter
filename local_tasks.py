from invoke import task


# create your local tasks here
# these will be added by tasks.py
@task
def build(c, service=""):
    c.run(f"docker-compose --env-file .env -f docker-compose.yml {service} build")


@task
def up(c, service=None):
    if service:
        c.run(
            f"docker-compose --env-file .env -f docker-compose.yml restart {service}",
            pty=True,
        )
    else:
        c.run("docker-compose --env-file .env -f docker-compose.yml up", pty=True)


@task
def down(c, service=""):
    if service:
        c.run(f"docker-compose --env-file .env -f docker-compose.yml stop {service}")
    else:
        c.run("docker-compose --env-file .env -f docker-compose.yml down")


@task
def manage(c, cmd):
    c.run(
        f"docker-compose --env-file .env -f docker-compose.yml exec web python manage.py {cmd}",
        pty=True,
    )


@task
def gen_tags(c):
    c.run("ctags -R --fields=+l --languages=python --python-kinds=-iv ./ $VIRTUAL_ENV/")


@task
def test(c, service):
    opt = f"{service}"
    print(opt)


@task
def generate_environment(c):
    c.run("ansible-playbook deploy/playbooks/local_site.yml")
