#!/usr/bin/env python3

import logging
import os
import unittest
import shutil

# local modules
import deps_mgr

TEST_RESOURCES_DIR = "test_resources"

class TestSuite(unittest.TestCase):

    def test_simple_git_repo(self):
        ''' Very simple test procedure idea:
        1. remove deps DEPS_DIR
        2. download git repo defined in test_resources/simple_test_git dependency file
        3. check if file A.txt (that's available on master branch) exists -> this means test is successful
        '''
        
        # path to test directory
        TEST_PATH = os.path.join(TEST_RESOURCES_DIR,"simple_git_test")
        # path to A.txt file
        TEST_FILE = os.path.join(deps_mgr.DEPS_DIR, "test_repo", "A.txt")
        
        # test start:
        shutil.rmtree(deps_mgr.DEPS_DIR, ignore_errors=True)
        deps_mgr.get_deps(TEST_PATH)
        self.assertTrue(os.path.isfile(TEST_FILE))

        #cleanup 
        shutil.rmtree(deps_mgr.DEPS_DIR, ignore_errors=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()