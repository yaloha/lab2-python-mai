from unittest.mock import patch

import pytest
import tempfile
import os

import typer
from typer.testing import CliRunner
from src.main import create_app

runner = CliRunner()
app = create_app()


class TestCatCommand:
    def test_cat_success(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("meow meow\nmrow mrow")
            temp = f.name
        try:
            result = runner.invoke(app, ["cat", temp])
            assert "meow meow" in result.stdout
            assert "mrow mrow" in result.stdout
        finally:
            os.remove(temp)

    def test_cat_nonexistent(self):
        result = runner.invoke(app, ["cat", "nonexistent_file.txt"])
        assert "cat: nonexistent_file.txt: no such file" in result.stderr.lower()

    def test_cat_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = runner.invoke(app, ["cat", temp_dir])
            assert f"cat: {temp_dir}: no such file".lower() in result.stderr.lower()

    def test_cat_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w') as f:
            temp = f.name
            result = runner.invoke(app, ["app", temp])
            assert result.stdout == ""

class TestCpCommand:
    def test_cp_ftf(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("meow")
            path_from = file.name

        path_to = path_from + "1"

        try:
            result = runner.invoke(app, ["cp", path_from, path_to])
            assert os.path.exists(path_to)
            with open(path_to, 'r') as f:
                assert f.read() == "meow"
        finally:
            os.remove(path_from)
            os.remove(path_to)

    def test_cp_ftd(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("meow")
            file_from = file.name

        with tempfile.TemporaryDirectory() as dest_dir:
            result = runner.invoke(app, ["cp", file_from, dest_dir])
            file_to = os.path.join(dest_dir, os.path.basename(file_from))
            assert os.path.exists(file_to)
            with open(file_to, 'r') as f:
                assert f.read() == "meow"
            os.remove(file_from)

    def test_cp_dir_wo_flag(self):
        with tempfile.TemporaryDirectory() as source_dir:
            result = runner.invoke(app, ["cp", source_dir, "/meow/dest"])
            assert "cp: use -r flag to copy a directory" in result.stderr.lower()


class TestMvCommand:
    def test_mv_f_rename(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("meow")
            path_from = file.name
        path_to = path_from + "1"
        try:
            result = runner.invoke(app, ["mv", path_from, path_to])
            assert not os.path.exists(path_from)
            assert os.path.exists(path_to)
            with open(path_to, 'r') as f:
                assert f.read() == "meow"
        finally:
            os.remove(path_to)

    def test_mv_ftd(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("meow")
            file_from = file.name
        with tempfile.TemporaryDirectory() as dest_dir:
            result = runner.invoke(app, ["mv", file_from, dest_dir])
            file_to = os.path.join(dest_dir, os.path.basename(file_from))
            assert not os.path.exists(file_from)
            assert os.path.exists(file_to)
            with open(file_to, 'r') as f:
                assert f.read() == "meow"

    def test_mv_dir(self):
        with tempfile.TemporaryDirectory() as source_dir:
            with tempfile.TemporaryDirectory() as dest_parent:
                test_file = os.path.join(source_dir, "meow.txt")
                with open(test_file, 'w') as f:
                    f.write("meow")
                dest_dir = os.path.join(dest_parent, "moved_dir")
                result = runner.invoke(app, ["mv", source_dir, dest_dir])
                assert not os.path.exists(source_dir)
                assert os.path.exists(dest_dir)
                assert os.path.exists(os.path.join(dest_dir, "meow.txt"))

    def test_mv_dtd(self):
        with tempfile.TemporaryDirectory() as source_dir:
            with tempfile.TemporaryDirectory() as dest_dir:
                result = runner.invoke(app, ["mv", source_dir, dest_dir])
                expected_path = os.path.join(dest_dir, os.path.basename(source_dir))
                assert not os.path.exists(source_dir)
                assert os.path.exists(expected_path)

    def test_mv_nonexistent(self):
        result = runner.invoke(app, ["mv", "/nonexistent", "/destination"])
        assert "mv: /nonexistent: no such file or directory" in result.stderr.lower()

    def test_mv_overwrite(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("original")
            path_from = file.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
            file1.write("fake")
            path_to = file1.name

        try:
            result = runner.invoke(app, ["mv", path_from, path_to])
            assert not os.path.exists(path_from)
            assert os.path.exists(path_to)
            with open(path_to, 'r') as f:
                assert f.read() == "original"
        finally:
            os.remove(path_to)

class TestRmCommand:
    def test_rm_w_confirm(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("meow")
            path = file.name
        try:
            with patch('builtins.input', return_value='Y'):
                result = runner.invoke(app, ["rm", path])
                assert not os.path.exists(path)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_rm_wo_confirm(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write("meow")
            path = file.name
        try:
            with patch('builtins.input', return_value='n'):
                result = runner.invoke(app, ["rm", path])
                assert os.path.exists(path)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_rm_dir_wo_flag(self):
        with tempfile.TemporaryDirectory() as dir_path:
            with patch('builtins.input', return_value='Y'):
                result = runner.invoke(app, ["rm", dir_path])
                assert os.path.exists(dir_path)

    def test_rm_dir_w_flag(self):
        """Test removing directory with -r flag and confirmation"""
        with tempfile.TemporaryDirectory() as dir_path:
            test_file = os.path.join(dir_path, "test.txt")
            with open(test_file, 'w') as f:
                f.write("meow")
            with patch('builtins.input', return_value='Y'):
                result = runner.invoke(app, ["rm", "-r", dir_path])
                assert not os.path.exists(dir_path)

    def test_rm_nonexistent(self):
        result = runner.invoke(app, ["rm", "/nonexistent"])
        assert "no such file/directory" in result.output.lower()


class TestCdCommand:
    @patch('os.chdir')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_cd_valid_dir(self, mock_exp_path, mock_check_dir_exists, mock_chdir):
        mock_exp_path.return_value = "/meow/path"
        mock_check_dir_exists.return_value = True
        result = runner.invoke(app, ["cd", "/meow/path"])
        mock_exp_path.assert_called_once_with("/meow/path")
        mock_chdir.assert_called_once_with("/meow/path")

    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_cd_nonexistent_dir(self, mock_exp_path, mock_check_dir_exists):
        mock_exp_path.return_value = "/invalid/mrow"
        mock_check_dir_exists.return_value = False
        result = runner.invoke(app, ["cd", "/invalid/mrow"])
        mock_exp_path.assert_called_once_with("/invalid/mrow")
        mock_check_dir_exists.assert_called_once_with("/invalid/mrow", "cd", 1)

    @patch('os.chdir')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_cd_permission_err(self, mock_exp_path, mock_check_dir_exists, mock_chdir):
        mock_exp_path.return_value = "/restricted/mrow"
        mock_check_dir_exists.return_value = True
        mock_chdir.side_effect = PermissionError("Permission denied")
        result = runner.invoke(app, ["cd", "/restricted/mrow"])
        assert "cd: /restricted/mrow: Permission denied" in result.output

    @patch('os.chdir')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_cd_curr_dir(self, mock_exp_path, mock_check_dir_exists, mock_chdir):
        mock_exp_path.return_value = "."
        mock_check_dir_exists.return_value = True
        result = runner.invoke(app, ["cd"])
        mock_exp_path.assert_called_once_with(".")
        mock_check_dir_exists.assert_called_once_with(".", "cd", 1)
        mock_chdir.assert_called_once_with(".")

    @patch('os.chdir')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_cd_err(self, mock_exp_path, mock_check_dir_exists, mock_chdir):
        mock_exp_path.return_value = "/problematic/mrow"
        mock_check_dir_exists.return_value = True
        mock_chdir.side_effect = Exception("Unexpected error")
        result = runner.invoke(app, ["cd", "/problematic/mrow"])
        assert "cd: /problematic/mrow: Unexpected error" in result.output


class TestLsCommand:
    @patch('os.listdir')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_ls_current_dir(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_listdir):
        mock_exp_path.return_value = "."
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = True
        mock_listdir.return_value = ["meow.txt", "mrow.py", "dir"]
        result = runner.invoke(app, ["ls"])
        mock_exp_path.assert_called_once_with(".")
        mock_check_dir_exists.assert_called_once_with(".", "ls", 1)
        mock_check_permission.assert_called_once_with(".", "ls")
        mock_listdir.assert_called_once_with(".")
        assert "meow.txt" in result.output
        assert "mrow.py" in result.output
        assert "dir" in result.output

    @patch('os.listdir')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_ls_nonexistent_dir(self, mock_exp_path, mock_check_dir_exists, mock_listdir):
        mock_exp_path.return_value = "/nonexistent/meow"
        mock_check_dir_exists.return_value = False
        result = runner.invoke(app, ["ls", "/nonexistent/meow"])
        mock_exp_path.assert_called_once_with("/nonexistent/meow")
        mock_check_dir_exists.assert_called_once_with("/nonexistent/meow", 'ls', 1)
        mock_listdir.assert_not_called()

    @patch('os.listdir')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_ls_dir_perm_err(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_listdir):
        mock_exp_path.return_value = "/restricted/mrow"
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = False
        result = runner.invoke(app, ["ls", "/restricted/mrow"])
        mock_exp_path.assert_called_once_with("/restricted/mrow")
        mock_check_dir_exists.assert_called_once_with("/restricted/mrow", 'ls', 1)
        mock_check_permission.assert_called_once_with("/restricted/mrow", 'ls')
        mock_listdir.assert_not_called()

    @patch('os.listdir')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_ls_generic_exception(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_listdir):
        mock_exp_path.return_value = "/problematic/mrow"
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = True
        mock_listdir.side_effect = Exception("Unexpected error")
        result = runner.invoke(app, ["ls", "/problematic/mrow"])
        mock_exp_path.assert_called_once_with("/problematic/mrow")
        mock_check_dir_exists.assert_called_once_with("/problematic/mrow", 'ls', 1)
        mock_check_permission.assert_called_once_with("/problematic/mrow", 'ls')
        mock_listdir.assert_called_once_with("/problematic/mrow")