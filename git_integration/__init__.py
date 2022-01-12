import logging
from git import Repo


def git_add_commit_push():
    repo = Repo('.git')
    git = repo.git
    git.add('README.md')
    git.add('useragents.json')
    repo.index.commit('Update useragents')
    origin = repo.remote(name='origin')
    origin.push()
    logging.info('Git commit and push success.')
