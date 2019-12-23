import logging
import sys
from os import environ, getcwd
from os.path import join as path_join

from . import cli, create, generate, list


class ConstraintManager:
    """The ConstraintManager class implements the frontend interface to the
    constraint manager.

    It primarily control input/output locations. By default it searches
    in a repository contained in the tool and
    `pwd`/constraint_manager_out (default export location). Set the
    environment variable CONSTRAINT_MANAGER_LOCAL_REPO to modify the
    location of the latter.
    """

    def __init__(self, argv=None):
        if 'CONSTRAINT_MANAGER_LOCAL_REPO' not in environ:
            environ['CONSTRAINT_MANAGER_LOCAL_REPO'] = path_join(
                getcwd(), 'constraint_manager_out')
        if argv is None:
            argv = sys.argv[1:]

        args = cli.parse_args(argv)
        self._configure_logging(args.log_level)

        # This is a little obfuscated, but grabs the function to call for the command
        # of the form command.command()
        cmd_function = getattr(globals()[args.command], args.command)
        cmd_function(args)

    @staticmethod
    def _configure_logging(log_level):
        """Configure logging based on log_level string."""
        level = getattr(logging, log_level.upper())
        logging.basicConfig(
            filename=None, format="%(levelname)7s - %(message)s", level=level
        )


def main():
    # console_scripts tags onto main func, do not remove
    constraint_manager = ConstraintManager()


if __name__ == '__main__':
    sys.path.append('..')
    main()
