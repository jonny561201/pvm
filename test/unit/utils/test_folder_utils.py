from pathlib import Path

import pytest
from mock import patch, Mock

from svc.utilities.folder_utils import find_python_version, get_python_version_folders


@patch('svc.utilities.folder_utils.File.VERSION_DIR')
def test_find_python_version__no_directory(dir_mock):
    version = '3.1.12'
    dir_mock.exists.return_value = False

    with pytest.raises(ValueError) as er:
        find_python_version(version)

    assert str(er.value) == f'python {version} is not installed'


@patch('svc.utilities.folder_utils.File.VERSION_DIR')
def test_get_python_version_folders__should_return_empty_if_no_directory(dir_mock):
    dir_mock.exists.return_value = False
    actual = get_python_version_folders()

    assert actual  == []


@patch('svc.utilities.folder_utils.File.VERSION_DIR')
def test_get_python_version_folders__should_return_matching_directories(dir_mock):
    path_one = __create_mock_path('python-3.10.12')
    path_two = __create_mock_path('python-3.11.8')
    path_three = __create_mock_path('not-a-version')

    dir_mock.exists.return_value = True
    dir_mock.iterdir.return_value = [path_one, path_two, path_three]
    actual = get_python_version_folders()

    assert actual == [path_one, path_two]


@patch('svc.utilities.folder_utils.File.VERSION_DIR')
def test_get_python_version_folders__should_only_return_directories(dir_mock):
    path_one = __create_mock_path('python-3.10.12', False)
    path_two = __create_mock_path('python-3.11.8', True)

    dir_mock.exists.return_value = True
    dir_mock.iterdir.return_value = [path_one, path_two]
    actual = get_python_version_folders()

    assert actual == [path_two]


def __create_mock_path(name: str, is_dir: bool = True):
    path = Mock(spec=Path)
    path.name = name
    path.exists.return_value = True
    path.is_dir.return_value = is_dir

    return path