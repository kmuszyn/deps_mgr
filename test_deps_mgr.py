#!/usr/bin/env python3

import logging
import os
import shutil
import unittest

# local modules
import deps_mgr

TEST_RESOURCES_DIR = "test_resources"
TEST_DIR = "test_dir"

def copy_and_rename_config_file(config_file_path, dest_dir):
    dest_path = os.path.join(dest_dir, deps_mgr.DEPS_FILE)
    shutil.copy(config_file_path, dest_path)

# class TestSuite(unittest.TestCase):

#     def setUp(self):
#         shutil.rmtree(deps_mgr.DEPS_DIR, ignore_errors=True)
#         shutil.rmtree(TEST_DIR, ignore_errors=True)
#         os.makedirs(TEST_DIR)

#     def tearDown(self):
#         shutil.rmtree(deps_mgr.DEPS_DIR, ignore_errors=True)
#         shutil.rmtree(TEST_DIR, ignore_errors=True)

#     def test_simple_git_repo(self):
#         ''' Test basic git cloning of repo to empty dir.
#         Steps:
#         1. remove deps DEPS_DIR
#         2. download git repo defined in test_resources/simple_test_git dependency file
#         3. check if file A.txt (that's available on master branch) exists -> this means test is successful
#         '''
#         copy_and_rename_config_file(os.path.join(TEST_RESOURCES_DIR, "simple_git_test.cfg"), TEST_DIR)

#         # path to A.txt file
#         TEST_FILE = os.path.join(deps_mgr.DEPS_DIR, "test_repo", "A.txt")
        
#         # test start:
#         deps_mgr.get_deps(TEST_DIR)
#         self.assertTrue(os.path.isfile(TEST_FILE))

#     def test_git_existing_repository(self):
#         ''' 
#         Steps:
#         1. clone a repo
#         2. re-run get deps with existing repo
#         TODO
#         '''
#         copy_and_rename_config_file(os.path.join(TEST_RESOURCES_DIR, "simple_git_test.cfg"), TEST_DIR)

#         # path to A.txt file
#         TEST_FILE = os.path.join(deps_mgr.DEPS_DIR, "test_repo", "A.txt")
        
#         # test start:
#         deps_mgr.get_deps(TEST_DIR)
#         self.assertTrue(os.path.isfile(TEST_FILE))

#         deps_mgr.get_deps(TEST_DIR)

class ConfigLoaderTest(unittest.TestCase):

    def test_load_repository_list(self):
        TEST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository_list.yaml")
        repositories = deps_mgr.parse_repositories_list(TEST_FILE)
        self.assertEqual(repositories[0].name, "test_repository")
        self.assertEqual(repositories[0].location, "test_repository.yaml")

    def test_load_repository(self):
        TEST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository.yaml")
        repository_data = deps_mgr.parse_repository_data(TEST_FILE)

        self.assertEqual(repository_data.get_url(component = "libgui", version = "1.0.0.0"), "http://url_to_1.0.0.0.zip")
        self.assertEqual(repository_data.get_url(component = "libgui", version = "1.1.0.0"), "http://url_to_1.1.0.0.zip")
        self.assertEqual(repository_data.get_url(component = "libgui", version = "git"), "http://git_repo_path.git")
        self.assertEqual(repository_data.get_url(component = "my_app", version = "1.0.0.0"), "http://link_to_app_package_1.0.0.0.zip")
        self.assertEqual(repository_data.get_url(component = "libnetwork", version = "1.0.0.0"), "http://libnetwork/1.0.0.0.zip")

        self.assertEqual(repository_data.get_dependencies(component = "my_app", version = "1.0.0.0"), 
            [{"component" : "libgui", "version" : "1.0.0.0"}])

        self.assertEqual(repository_data.get_dependencies(component = "my_app", version = "1.2.0.0"), 
            [{"component" : "libgui", "version" : "1.1.0.0"}, {"component" : "libnetwork", "version" : "1.0.0.0"}])

        self.assertEqual(repository_data.get_dependencies(component = "libnetwork", version = "1.0.0.0"), [])

    def test_load_dependencies(self):
        TEST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_dependencies.yaml")
        dependencies = deps_mgr.parse_dependencies(TEST_FILE)
        self.assertTrue("depends" in dependencies)

        self.assertTrue("libgui" in dependencies["depends"])
        self.assertTrue("version" in dependencies["depends"]["libgui"])
        self.assertEqual(dependencies["depends"]["libgui"]["version"], "1.0.0.0")

        self.assertTrue("libnetwork" in dependencies["depends"])
        self.assertTrue("version" in dependencies["depends"]["libnetwork"])
        self.assertEqual(dependencies["depends"]["libnetwork"]["version"], "1.0.0.0")

class GitDependencyDownloadTest(unittest.TestCase):

    def do_not_run_yet():

        REPOSITORY_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository.yaml")
        deps_repository = Repository()
        deps_repository.add_repository_config_file(REPOSITORY_FILE)

        DEPS_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_dependencies.yaml")


        deps_mgr = DepsMgr()
        deps_mgr.set_repository_list(REPOSITORY_LIST_FILE)
        deps_mgr.load_repositories()
        deps_mgr.get_dependencies(DEPS_FILE)

        # md5 of output with git repo

        # classes:
        # Repository - maintains information about where we can download a component
        # Dependency - contains name, version + additional parameters (if git, then branch & commit)
        # 
        # Repository.get_dependency_info(dependency) -> should return information about the dependency
        # with a location and additional dependencies (?)
        # actually a dependecy info implies what component list is required
        # so repository should return a full list I think
        # but: dependencies may have a longer list of components...

'''
test ideas:
adding multiple repositories
    with conflicting items

dependency not present in any repository
'''

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()