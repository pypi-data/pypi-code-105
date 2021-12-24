import contextlib
import io
import os
import tempfile
import unittest

from lesana import command
from . import utils


class Args:
    def __init__(self, args):
        self.args = args

    def __getattribute__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            try:
                return self.args[k]
            except KeyError as e:
                raise AttributeError(e)


class CommandsMixin:
    def _edit_file(self, filepath):
        return True

    def _run_command(self, cmd, args):
        stream = {
            'stdout': io.StringIO(),
            'stderr': io.StringIO(),
        }
        cmd.edit_file_in_external_editor = self._edit_file
        cmd.args = Args(args)
        with contextlib.redirect_stdout(stream['stdout']):
            with contextlib.redirect_stderr(stream['stderr']):
                cmd.main()
        return stream


class testCommandsSimple(unittest.TestCase, CommandsMixin):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        utils.copytree(
            'tests/data/simple',
            self.tmpdir.name,
            dirs_exist_ok=True,
        )

    def tearDown(self):
        pass

    def test_init(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
        }
        streams = self._run_command(command.Init(), args)
        self.assertEqual(streams['stdout'].getvalue(), '')
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_new(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
        }
        streams = self._run_command(command.New(), args)
        self.assertEqual(len(streams['stdout'].getvalue()), 33)
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_edit(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'eid': '11189ee4',
        }
        streams = self._run_command(command.Edit(), args)
        self.assertTrue(args['eid'] in streams['stdout'].getvalue())
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_show(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'eid': '11189ee4',
            'template': False,
        }
        streams = self._run_command(command.Show(), args)
        self.assertTrue(
            'name: Another item' in streams['stdout'].getvalue()
        )
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_index(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'files': None,
            'reset': True,
        }
        streams = self._run_command(command.Index(), args)
        self.assertEqual(
            streams['stdout'].getvalue(),
            'Found and indexed 3 entries\n',
        )
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_search(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'template': False,
            'query': 'Another',
            'offset': None,
            'pagesize': None,
            'sort': None,
            'expand_query_template': False,
            'all': False,
        }
        streams = self._run_command(command.Search(), args)
        self.assertTrue(
            '11189ee4' in streams['stdout'].getvalue()
        )
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_get_values(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'template': False,
            'query': '*',
            'field': 'position',
        }
        streams = self._run_command(command.GetValues(), args)
        self.assertIn('somewhere: 2', streams['stdout'].getvalue())
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_export(self):
        dest_tmpdir = tempfile.TemporaryDirectory()
        utils.copytree(
            'tests/data/simple',
            dest_tmpdir.name,
            dirs_exist_ok=True,
        )
        # TODO: make finding the templates less prone to breaking and
        # then remove the cwd change from here
        old_cwd = os.getcwd()
        os.chdir(self.tmpdir.name)
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'template': 'templates/from_self.yaml',
            'query': 'Another',
            'destination': dest_tmpdir.name,
        }
        streams = self._run_command(command.Export(), args)
        os.chdir(old_cwd)
        self.assertEqual(streams['stdout'].getvalue(), '')
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_remove(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'entries': '11189ee4',
        }
        streams = self._run_command(command.Remove(), args)
        self.assertEqual(streams['stdout'].getvalue(), '')
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_update(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'query': 'Another',
            'field': 'position',
            'value': 'here',
        }
        streams = self._run_command(command.Update(), args)
        self.assertEqual(streams['stdout'].getvalue(), '')
        self.assertEqual(streams['stderr'].getvalue(), '')


class testCommandsComplex(unittest.TestCase, CommandsMixin):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        utils.copytree(
            'tests/data/complex',
            self.tmpdir.name,
            dirs_exist_ok=True,
        )

    def tearDown(self):
        pass

    def test_get_values_from_list(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'template': False,
            'query': '*',
            'field': 'tags',
        }
        streams = self._run_command(command.GetValues(), args)
        self.assertIn('this: 1', streams['stdout'].getvalue())
        self.assertEqual(streams['stderr'].getvalue(), '')

    def test_search_template(self):
        args = {
            'collection': self.tmpdir.name,
            'git': True,
            'template': False,
            'query': '{{ nice }}',
            'expand_query_template': True,
            'offset': None,
            'pagesize': None,
            'sort': None,
            'all': False,
        }
        streams = self._run_command(command.Search(), args)
        self.assertIn('8e9fa1ed', streams['stdout'].getvalue())
        self.assertIn('5084bc6e', streams['stdout'].getvalue())
        self.assertEqual(streams['stderr'].getvalue(), '')


if __name__ == '__main__':
    unittest.main()
