#!/usr/bin/env python
import os

from fabric.api import cd, lcd, run, sudo, env, local, put
from fabric.context_managers import prefix

env.use_ssh_config = True
env.hosts = ["odesk-aws"]

LOCAL_PROJECT_DIR = os.path.join(os.path.dirname(__file__), "project")
REMOTE_PROJECT_DIR = "/home/ubuntu/candidates_emailer"


def deploy():
    with cd(LOCAL_PROJECT_DIR):
        local("git push")
    
    with prefix("source {0}".format(os.path.join(
        REMOTE_PROJECT_DIR, "..", ".virtualenvs", "odesk", "bin", "activate"))):
        with cd(REMOTE_PROJECT_DIR):
            run("git pull")
