import argparse

from svc.services.install_service import install_latest_release, get_python_versions, set_default_version


def execute_commands(args: argparse.Namespace):
    if args.command == 'use':
        print('Hello world')
    elif args.command == 'install':
        install_latest_release(args.python_version)
    elif args.command == 'list':
        get_python_versions()
    elif args.command == 'default':
        set_default_version(args.python_version)


def register_commands(parser: argparse.ArgumentParser):
    parser.add_argument('--version', '-V', action='version', version='1.00', help='Version of PVM installed')
    subparsers = parser.add_subparsers(dest='command', required=True)
    _register_subcommands(subparsers)


def _register_subcommands(subparsers: argparse._SubParsersAction):
    use_parser = subparsers.add_parser('use', help='Select Python version')
    use_parser.add_argument('python_version', help='Version to use (e.g. 3.12)')

    subparsers.add_parser('list', help='List installed Python versions')

    install_parser = subparsers.add_parser('install', help='Install a new Python version')
    install_parser.add_argument('python_version', help='Version to install (e.g. 3.12)')

    default_parser = subparsers.add_parser('default', help='Set the global Python default')
    default_parser.add_argument('python_version', help='Version to use (e.g. 3.12)')