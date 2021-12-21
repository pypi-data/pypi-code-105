import os
import shutil
from click.testing import CliRunner
from resetmigrations import resetmigrations
import unittest


CONST_SAMPLE_FILES_FROM_DIR_NAME = "sample-files"
CONST_SAMPLE_FILES_TO_DIR_NAME = "tests/sample-files"
CONST_SAMPLE_FILES_TESTS_DIR_NAME = "tests"


class ResetMigrationsCleanTest(unittest.TestCase):

    def setUp(self):
        self.prepare_testing_files()

    def prepare_testing_files(self):
        self.scriptsDirectory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.scriptsDirectory)
        os.chdir("..")
        fromDirectory = os.getcwd() + "/" + CONST_SAMPLE_FILES_FROM_DIR_NAME
        toDirectory = os.getcwd() + "/" + CONST_SAMPLE_FILES_TO_DIR_NAME
        print(fromDirectory)
        print(toDirectory)
        shutil.rmtree(toDirectory, ignore_errors=True)
        shutil.copytree(fromDirectory, toDirectory)

    def test_clean_command_and_files_are_deleted(self):
        print(self.scriptsDirectory)
        runner = CliRunner()
        result = runner.invoke(
            resetmigrations,
            ['clean', '--path', self.scriptsDirectory + "/sample-files"]
        )
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
