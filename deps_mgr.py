#!/usr/bin/env python3

DEPS_DIR = "deps"
DEPS_FILE = "deps.cfg"

# config keys TODO move them somewhere
KEY_BRANCH = "branch"
KEY_DEPS = "deps"
KEY_NAME = "name"
KEY_TYPE = "type"
KEY_URL = "url"
KEY_VERSION = "version"

import logging
import os
import yaml

from git import Repo

log = logging.getLogger(__name__)

def get_test_repo():
    from git import Repo
    Repo.clone_from("https://github.com/kmuszyn/deps_test.git", "deps_test")

class GitRepoConfig():

    def __init__(self, repo_config):
        # TODO add config validatin
        self.name = repo_config[KEY_NAME]
        self.url = repo_config[KEY_URL]
        self.branch = repo_config[KEY_BRANCH]
        self.version = repo_config[KEY_VERSION]

def handle_git_dep(repo_config):
    log.debug("Getting git repository... name: %s", repo_config.name)
    REPO_DIR = os.path.join(DEPS_DIR, repo_config.name)

    repo = None
    if not os.path.exists(REPO_DIR):
        log.debug("Dir %s not present, cloning repository", REPO_DIR)
        repo = Repo.clone_from(repo_config.url, REPO_DIR)
    else:
        repo = Repo(REPO_DIR)
        log.debug("Repo already exists, branch: %s, commit: %s", repo.active_branch, repo.head.commit)

    if repo_config.branch:
        repo.git.checkout(repo_config.branch)
        repo.git.reset(repo_config.version)
        #todo add checking if commit exists on a branch

    # else: TODO add just checkout to commit (detached head)

def get_dep(dep_config):
    log.debug("Getting dependency: %s type: %s", dep_config[KEY_NAME], dep_config[KEY_TYPE])

    if dep_config[KEY_TYPE] == "git":
        handle_git_dep(GitRepoConfig(dep_config))

def read_config(dir):
    full_file_path = os.path.join(dir, DEPS_FILE)

    deps_config = {}
    with open(full_file_path,"r") as f:
        deps_config = yaml.safe_load(f)

    log.debug("Got %s deps", len(deps_config[KEY_DEPS]))
    for dep in deps_config[KEY_DEPS]:
        get_dep(dep)

def get_deps(dir):
    deps_config = read_config(dir)

class RepositoryData:
    repository_data = dict()
    
    def __init__(self, repository_file):
        with open(repository_file, "r") as f:
            self.repository_data = yaml.safe_load(f)

    def get_url(self, component, version):
        return self.repository_data[component][version]["url"]

    def get_dependencies(self, component, version):
        component_details = self.repository_data[component][version]
        
        if "depends" not in component_details:
            return []

        deps = self.repository_data[component][version]["depends"]
        result = []
        for d in deps:
            result.append(dict(zip(["component","version"],  d.split(" "))))

        return result

def parse_repository_data(repo_file):
    repository_data = RepositoryData(repo_file)
    return repository_data

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    get_deps(".")