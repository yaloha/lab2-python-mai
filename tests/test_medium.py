from unittest.mock import patch, mock_open

import pytest
import tempfile
import os

import typer
from typer.testing import CliRunner
from src.main import create_app

runner = CliRunner()
app = create_app()


class TestZipUnzipCommands:
    @patch('shutil.make_archive')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_zip_success(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_make_archive):
        mock_exp_path.side_effect = ["/test/dir", "/test/meow"]
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = True
        result = runner.invoke(app, ["zip", "/test/dir", "/test/meow"])
        mock_exp_path.assert_any_call("/test/dir")
        mock_exp_path.assert_any_call("/test/meow")
        mock_check_dir_exists.assert_called_once_with("/test/dir", "zip", 1)
        mock_check_permission.assert_called_once_with("/test/dir", "zip")
        mock_make_archive.assert_called_once_with("/test/meow", 'zip', "/test/dir")

    @patch('shutil.make_archive')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_zip_nonexistent_dir(self, mock_exp_path, mock_check_dir_exists, mock_make_archive):
        mock_exp_path.return_value = "/nonexistent/dir"
        mock_check_dir_exists.return_value = False
        result = runner.invoke(app, ["zip", "/nonexistent/dir", "meow"])
        mock_check_dir_exists.assert_called_once_with("/nonexistent/dir", "zip", 1)
        mock_make_archive.assert_not_called()

    @patch('shutil.make_archive')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_zip_permission_err(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_make_archive):
        mock_exp_path.return_value = "/restricted/dir"
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = False
        result = runner.invoke(app, ["zip", "/restricted/dir", "meow"])
        mock_check_permission.assert_called_once_with("/restricted/dir", "zip")
        mock_make_archive.assert_not_called()

    @patch('shutil.unpack_archive')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_file_exists')
    @patch('src.path_f.exp_path')
    def test_unzip_success(self, mock_exp_path, mock_check_file_exists, mock_check_permission, mock_unpack_archive):
        mock_exp_path.return_value = "/test/meow.zip"
        mock_check_file_exists.return_value = True
        mock_check_permission.return_value = True
        result = runner.invoke(app, ["unzip", "/test/meow.zip"])
        mock_exp_path.assert_called_once_with("/test/meow.zip")
        mock_check_file_exists.assert_called_once_with("/test/meow.zip", "unzip", 1)
        mock_check_permission.assert_called_once_with("/test/meow.zip", "unzip")
        mock_unpack_archive.assert_called_once_with("/test/meow.zip", '.', 'zip')

    @patch('shutil.unpack_archive')
    @patch('src.path_f.check_file_exists')
    @patch('src.path_f.exp_path')
    def test_unzip_nonexistent_file(self, mock_exp_path, mock_check_file_exists, mock_unpack_archive):
        mock_exp_path.return_value = "/nonexistent/meow.zip"
        mock_check_file_exists.return_value = False
        result = runner.invoke(app, ["unzip", "/nonexistent/meow.zip"])
        mock_check_file_exists.assert_called_once_with("/nonexistent/meow.zip", "unzip", 1)
        mock_unpack_archive.assert_not_called()


class TestTarUntarCommands:
    @patch('shutil.make_archive')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_tar_success(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_make_archive):
        mock_exp_path.side_effect = ["/test/dir", "/test/meow"]
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = True
        result = runner.invoke(app, ["tar", "/test/dir", "/test/meow"])
        mock_exp_path.assert_any_call("/test/dir")
        mock_exp_path.assert_any_call("/test/meow")
        mock_check_dir_exists.assert_called_once_with("/test/dir", "tar", 1)
        mock_check_permission.assert_called_once_with("/test/dir", "tar")
        mock_make_archive.assert_called_once_with("/test/meow", 'tar', "/test/dir")

    @patch('shutil.make_archive')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_tar_nonexistent_dir(self, mock_exp_path, mock_check_dir_exists, mock_make_archive):
        mock_exp_path.return_value = "/nonexistent/dir"
        mock_check_dir_exists.return_value = False
        result = runner.invoke(app, ["tar", "/nonexistent/dir", "meow"])
        mock_check_dir_exists.assert_called_once_with("/nonexistent/dir", "tar", 1)
        mock_make_archive.assert_not_called()

    @patch('shutil.make_archive')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_dir_exists')
    @patch('src.path_f.exp_path')
    def test_tar_permission_err(self, mock_exp_path, mock_check_dir_exists, mock_check_permission, mock_make_archive):
        mock_exp_path.return_value = "/restricted/dir"
        mock_check_dir_exists.return_value = True
        mock_check_permission.return_value = False
        result = runner.invoke(app, ["tar", "/restricted/dir", "meow"])
        mock_check_permission.assert_called_once_with("/restricted/dir", "tar")
        mock_make_archive.assert_not_called()

    @patch('shutil.unpack_archive')
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_file_exists')
    @patch('src.path_f.exp_path')
    def test_untar_success(self, mock_exp_path, mock_check_file_exists, mock_check_permission, mock_unpack_archive):
        mock_exp_path.return_value = "/test/meow.tar"
        mock_check_file_exists.return_value = True
        mock_check_permission.return_value = True
        result = runner.invoke(app, ["untar", "/test/meow.tar"])
        mock_exp_path.assert_called_once_with("/test/meow.tar")
        mock_check_file_exists.assert_called_once_with("/test/meow.tar", "untar", 1)
        mock_check_permission.assert_called_once_with("/test/meow.tar", "untar")
        mock_unpack_archive.assert_called_once_with("/test/meow.tar", '.', 'tar')

    @patch('shutil.unpack_archive')
    @patch('src.path_f.check_file_exists')
    @patch('src.path_f.exp_path')
    def test_untar_nonexistent_file(self, mock_exp_path, mock_check_file_exists, mock_unpack_archive):
        mock_exp_path.return_value = "/nonexistent/meow.tar"
        mock_check_file_exists.return_value = False
        result = runner.invoke(app, ["untar", "/nonexistent/meow.tar"])
        mock_check_file_exists.assert_called_once_with("/nonexistent/meow.tar", "untar", 1)
        mock_unpack_archive.assert_not_called()


class TestGrepCommand:
    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_file_exists')
    @patch('os.path.exists')
    @patch('src.path_f.exp_path')
    def test_grep_file_success(self, mock_exp_path, mock_exists, mock_check_file_exists, mock_check_permission):
        mock_exp_path.return_value = "/test/meow.txt"
        mock_exists.return_value = True
        mock_check_file_exists.return_value = True
        mock_check_permission.return_value = True
        data = "line1\nbleh\nline3\n"
        with patch('builtins.open', mock_open(read_data=data)):
            result = runner.invoke(app, ["grep", "bleh", "/test/meow.txt"])
        assert "bleh" in result.output

    @patch('src.path_f.check_permission')
    @patch('src.path_f.check_file_exists')
    @patch('os.path.exists')
    @patch('src.path_f.exp_path')
    def test_grep_file_w_flag_i(self, mock_exp_path, mock_exists, mock_check_file_exists,
                                        mock_check_permission):
        mock_exp_path.return_value = "/test/meow.txt"
        mock_exists.return_value = True
        mock_check_file_exists.return_value = True
        mock_check_permission.return_value = True
        data = "line1\nMEOW\nline3\n"
        with patch('builtins.open', mock_open(read_data=data)):
            result = runner.invoke(app, ["grep", "meow", "/test/file.txt", "-i"])
        assert "MEOW" in result.output

    @patch('src.path_f.exp_path')
    def test_grep_nonexistent_path(self, mock_exp_path):
        mock_exp_path.return_value = "/nonexistent/meow"
        with patch('os.path.exists', return_value=False):
            result = runner.invoke(app, ["grep", "pattern", "/nonexistent/meow"])
        assert "no such path" in result.output
