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

###############################################################################################################

def parse_yaml(file_name):
    data = []
    with open(file_name, "r") as f:
        data = yaml.safe_load(f)
    return data

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

class PackageRepository:

    repositories = [] # this will be a list of Repository objects
    packages = dict()

    def set_repo_description_file(self, repository_list_file):
        self.repositories = parse_repo_description(repository_list_file)

    def update_repositories(self):
        # browsing all registered repositories
        for single_repo in self.repositories:
            # for a repository, getting latest data from repository location
            # right now file repo is supported only
            repo_packages = parse_yaml(single_repo.location)
            # todo check for overwrites here!
            self.packages.update(repo_packages)
                

    def prepare_download_list(self, input_packages):
        result = dict()
        for package, package_info in input_packages.items():
            package_version = package_info['version']
            # TODO duplicate checks!
            result[package] = package_version
            dependencies = self.get_dependencies(package, package_version)
            result.update(dependencies)
        return result

    def get_dependencies(self, package_name, package_version):
        if not package_name in self.packages:
            return dict()

        # packages is a map of
        # name -> version -> depends (list)
        version_related_info = self.packages[package_name][package_version]
        if 'depends' not in version_related_info:
            return dict()

        result = dict()
        package_dependencies = version_related_info['depends']
        for d in package_dependencies:
            name = d.split(" ")[0]
            version = d.split(" ")[1]
            result[name] = version
        return result


    def get_url(self, package, version):
        return self.packages[package][version]['url']


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