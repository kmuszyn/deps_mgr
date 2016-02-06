#!/usr/bin/env python3

import logging
import os
import unittest
import shutil

# local modules
import deps_mgr

TEST_RESOURCES_DIR = "test_resources"
TEST_DIR = "test_dir"

def copy_and_rename_config_file(config_file_path, dest_dir):
    dest_path = os.path.join(dest_dir, deps_mgr.DEPS_FILE)
    shutil.copy(config_file_path, dest_path)

class TestSuite(unittest.TestCase):

    def setUp(self):
        shutil.rmtree(deps_mgr.DEPS_DIR, ignore_errors=True)
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        os.makedirs(TEST_DIR)

    def tearDown(self):
        shutil.rmtree(deps_mgr.DEPS_DIR, ignore_errors=True)
        shutil.rmtree(TEST_DIR, ignore_errors=True)

    def test_simple_git_repo(self):
        ''' Test basic git cloning of repo to empty dir.
        Steps:
        1. remove deps DEPS_DIR
        2. download git repo defined in test_resources/simple_test_git dependency file
        3. check if file A.txt (that's available on master branch) exists -> this means test is successful
        '''
        copy_and_rename_config_file(os.path.join(TEST_RESOURCES_DIR, "simple_git_test.cfg"), TEST_DIR)

        # path to A.txt file
        TEST_FILE = os.path.join(deps_mgr.DEPS_DIR, "test_repo", "A.txt")
        
        # test start:
        deps_mgr.get_deps(TEST_DIR)
        self.assertTrue(os.path.isfile(TEST_FILE))

    def test_git_existing_repository(self):
        ''' 
        Steps:
        1. clone a repo
        2. re-run get deps with existing repo
        TODO
        '''
        copy_and_rename_config_file(os.path.join(TEST_RESOURCES_DIR, "simple_git_test.cfg"), TEST_DIR)

        # path to A.txt file
        TEST_FILE = os.path.join(deps_mgr.DEPS_DIR, "test_repo", "A.txt")
        
        # test start:
        deps_mgr.get_deps(TEST_DIR)
        self.assertTrue(os.path.isfile(TEST_FILE))

        deps_mgr.get_deps(TEST_DIR)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()