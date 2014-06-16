"""
This file runs all the tests.
You can run it directly using Jython, or by running 'ant test',
or you can run it from within JES by loading it and calling run_tests().
"""
import sys
import unittest
import os.path
import sys
import os
import fnmatch

def find(search_root, patterns=None, recurse=0, return_dirs=1):
    """
    Finds files/dirs rooted in a given directory that match a pattern.

    @param search_root: the root directory for the recursive search
    @param patterns: a list of shell-style patterns to search for
    @param recurse: whether to recurse into sub-directories of searchRoot
    @param return_dirs: whether to return directories that matched the pattern
    @return: a list of files(and possibly directories) rooted in searchRoot
                that match one of the supplied patterns or the empty list
                if no matches are found
    """
    if patterns is None:
        patterns = ["*"]

    matches = []

    for name in os.listdir(search_root):
        path = os.path.join(search_root, name)
        if not return_dirs and os.path.isdir(path):
            continue

        for pattern in patterns:
            if fnmatch.fnmatch(name, pattern):
                matches.append(name)
                break

    return matches


class DynamicStderrRedirectStream(object):
    def write(self, text):
        sys.stderr.write(text)


def run_tests():
    root_path = os.path.dirname(__file__)

    test_case_paths = find(root_path, ["Test_*.py", "test_*.py"], 0, 1)

    prefix_len = 0
    suffix_len = len(".py")

    if root_path not in sys.path:
        sys.path.append(root_path)

    test_cases = []
    for test_case_path in test_case_paths:
        test_case = test_case_path[prefix_len:-suffix_len].replace("/", ".")
        test_cases.append(test_case)

    unittest.defaultTestLoader.testMethodPrefix = "test"
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    master_test_suite = unittest.defaultTestLoader.loadTestsFromNames(
        test_cases)

    stream = DynamicStderrRedirectStream()
    suite_runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    return suite_runner.run(master_test_suite)


def main():
    result = run_tests()
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())

