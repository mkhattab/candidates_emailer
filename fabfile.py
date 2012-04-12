#!/usr/bin/env python
import os

from fabric.api import cd, lcd, run, sudo, env, local, put
from fabric.context_managers import prefix

env.use_ssh_config = True
env.hosts = ["odesk-aws"]
PROJECT_DIR = os.path.join(os.path.dirname(__file__), "project")


def test():
    run("echo $PWD")
