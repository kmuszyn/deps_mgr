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

def parse_yaml(file_name):
    data = []
    with open(file_name, "r") as f:
        data = yaml.safe_load(f)
    return data

def parse_dependencies(file_name):
    return parse_yaml(file_name)

class Repository:
    name = ""
    location = ""

    def __init__(self, name, location):
        self.name = name
        self.location = location


def parse_repo_description(file_name):
    result = []
    repositories_configuration = parse_yaml(file_name)
    for repository_dictionary in repositories_configuration["repositories"]:
        single_repo = Repository(
                repository_dictionary["name"], 
                repository_dictionary["location"]
            )
        result.append(single_repo)
    return result

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

def parse_repository_data(file_name):
    repository_data = RepositoryData(file_name)
    return repository_data

class PackageInfo:

    repositories = [] # this will be a list of Repository objects
    packages = dict()

    def set_repo_description_file(self, repository_list_file):
        self.repositories = parse_repo_description(repository_list_file)

    def update_repositories(self):
        # browsing all registered repositories
        for single_repo in self.repositories:
            # for a repository, getting latest data from repository location
            # right now file repo is supported only
            with open(single_repo.location, "r") as f:
                repo_packages = yaml.safe_load(f)
                # todo check for overwrites here!
                self.packages.update(repo_packages)

    def get_dependencies(self, package_name, package_version):
        print("\nchecking:", package_name, package_version)
        if not package_name in self.packages:
            return []

        version_related_info = self.packages[package_name][package_version]
        if 'depends' not in version_related_info:
            return []
        return version_related_info['depends']

class DependencyParser:
    '''
    Responsible for parsing denepdencies file.
    Stores dependency list, in future this may also store additional dependency configuration
    '''
    dependencies = dict()

    def parse(self, dependency_file):
        data = parse_yaml(dependency_file)
        self.dependencies = data['depends']

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)