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
        self.assertEqual(repositories["repositories"][0]["name"], "test_repository")
        self.assertEqual(repositories["repositories"][0]["location"], "test_repository.yaml")

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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()