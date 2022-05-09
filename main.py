import logging
import argparse

from core import update_all_from_remote, update_local_UA, ReadMe
from helper.logger import init_logging
from helper.exceptions import *
from git_integration import git_add_commit_push


def parse_args():
    args = {'quiet': False}
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False)
    arg_parser.add_argument('-l', '--log-level', action='store', dest='log_level', default='INFO')
    arg_parser.add_argument('-g', '--enable-git-integration', action='store_true', dest='git_integration', default=False)
    args = arg_parser.parse_args()
    return args


def main(args):
    try:
        result = update_all_from_remote()
    except Exception as e:
        logging.error(e, exc_info=True)
        input('\n\nPress any key to exit...')
        exit()
    readme = ReadMe()
    if result[0] > 0:
        update_local_UA(result[1], args.quiet)
        if args.git_integration:
            readme.update_time_and_ua(result[1])
    elif result[0] == -1:
        logging.info('UA fetch fatal error. Check your UA scrapping source. Exit.')
        input('\n\nPress any key to exit...')
        exit()
    else:
        logging.info('No new UA found.')
        if args.git_integration:
            readme.update_check_time()

    if args.git_integration:
        try:
            git_add_commit_push()
        except Exception as e:
            logging.error(e, exc_info=True)

    if not args.quiet:
        input('\n\nPress any key to exit...')
    exit()


if __name__ == '__main__':
    args = parse_args()
    init_logging(args.log_level)
    main(args)
