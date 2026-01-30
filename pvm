#!/usr/bin/env python3
import argparse

from svc.config.arg_config import register_commands, execute_commands


def main():
    parser = argparse.ArgumentParser(prog='pvm', description='python version manager')
    register_commands(parser)

    args = parser.parse_args()
    execute_commands(args)


if __name__ == '__main__':
    main()
