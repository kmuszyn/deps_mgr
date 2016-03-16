#!/usr/bin/env python3

import logging
import os
import unittest

# local modules
import deps_mgr

TEST_RESOURCES_DIR = "test_resources"

class UtilFunctionsTests(unittest.TestCase):

    def test_load_repository_description_function(self):
        TEST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository_list.yaml")
        repositories = deps_mgr.parse_repo_description(TEST_FILE)
        self.assertEqual(repositories[0].name, "test_repository")
        self.assertEqual(repositories[0].location, "test_resources/test_repository.yaml")

class PackageRepositoryTests(unittest.TestCase):

    def test_setting_repository_description_file(self):
        '''
        basic loading of simple repository description file
        it has only one repository named "test_repository"
        '''
        REPOSITORY_LIST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository_list.yaml")
        
        pkg_info = deps_mgr.PackageRepository()
        pkg_info.set_repo_description_file(REPOSITORY_LIST_FILE)
        self.assertEqual(1, len(pkg_info.repositories)) # there should be only one repo...
        self.assertEqual("test_repository", pkg_info.repositories[0].name) # with this name

    def test_update_repositories(self):
        REPOSITORY_LIST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository_list.yaml")
        pkg_info = deps_mgr.PackageRepository()
        pkg_info.set_repo_description_file(REPOSITORY_LIST_FILE)
        
        # repo is loaded, we can update repositories to get list of 
        # available packages
        pkg_info.update_repositories()
        self.assertTrue("libnetwork" in pkg_info.packages)
        self.assertTrue("my_app" in pkg_info.packages)
        self.assertTrue("libgui" in pkg_info.packages)

    def test_prepare_download_list(self):
        REPOSITORY_LIST_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_repository_list.yaml")
        
        pkg_info = deps_mgr.PackageRepository()
        pkg_info.set_repo_description_file(REPOSITORY_LIST_FILE)
        pkg_info.update_repositories()

        DEPS_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_dependencies.yaml")
        parser = deps_mgr.DependencyParser()
        parser.parse(DEPS_FILE)
        all_required_packages = pkg_info.prepare_download_list(parser.dependencies)
        
        for package, version in all_required_packages.items():
            url = pkg_info.get_url(package,version)
            print("Downloading {}-{} from {}".format(package, version,url))

        # TODO add meaningful asserts to make this a test...

class DependencyParserTests(unittest.TestCase):

    def test_dependency_file_parser(self):
        DEPS_FILE = os.path.join(os.getcwd(),TEST_RESOURCES_DIR,"test_dependencies.yaml")
        parser = deps_mgr.DependencyParser()
        parser.parse(DEPS_FILE)
        self.assertEqual(parser.dependencies['libgui']['version'], '1.0.0.0')
        self.assertEqual(parser.dependencies['libnetwork']['version'], '1.0.0.0')

'''
test ideas:
adding multiple repositories
    with conflicting items

dependency not present in any repository
'''

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()