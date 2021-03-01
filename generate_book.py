import re
from typing import Tuple

from jinja2 import Environment, FileSystemLoader

CSS_FILE = 'sample_css.css'
PAGES = [{
    'name': 'name', 'repos': ['repo'], 'comments': [{'author': 'iiogmgo', 'message': 'comments for you!'}]
}]


def get_css(filename: str) -> str:
    css = ''
    with open(filename) as f:
        css += f.read() + '\n'
    return css


def get_commits_by_repo(repos: list, name: str) -> Tuple[dict, dict, dict]:
    data = {}
    all_first_commit = None
    all_last_commit = None
    changes = re.compile(r'(\d+) files? changed(?:, (\d+) insertions?[(][+][)])?(?:, (\d+) deletions?)?')
    for repo in repos:
        with open(f'{repo}_{name.replace(" ", "_")}_log.txt') as f:
            r_commits = f.readlines()

        commits = []
        sum_changes, sum_inserts, sum_deletes = 0, 0, 0
        repo_first_commit = None
        repo_last_commit = None
        for r_commit in r_commits:
            splits = r_commit.split('::')
            change, insert, delete = re.search(changes, splits[4]).groups()
            commit = {
                'hash': splits[0],
                'title': splits[1],
                'date': splits[2],
                'author': splits[3],
                'changed': change or '-',
                'inserts': insert or '-',
                'deletes': delete or '-',
                'repo': repo,
            }
            commits.append(commit)
            sum_changes += int(change or 0)
            sum_inserts += int(insert or 0)
            sum_deletes += int(delete or 0)

            if not repo_first_commit or (repo_first_commit and repo_first_commit['date'] > commit['date']):
                repo_first_commit = commit
            if not repo_last_commit or (repo_last_commit and repo_last_commit['date'] < commit['date']):
                repo_last_commit = commit

        if not all_first_commit or (all_first_commit and all_first_commit['date'] > repo_first_commit['date']):
            all_first_commit = repo_first_commit
        if not all_last_commit or (all_last_commit and all_last_commit['date'] < repo_last_commit['date']):
            all_last_commit = repo_last_commit

        data[repo] = {
            'commits': commits, 'total_commits': len(commits),
            'total_changes': sum_changes, 'total_inserts': sum_inserts, 'total_deletes': sum_deletes,
            'range': f'{repo_first_commit["date"]} ~ {repo_last_commit["date"]}'
        }
    return data, all_first_commit, all_last_commit


for page in PAGES:
    ENV = Environment(loader=FileSystemLoader('.'))
    template = ENV.get_template('base.html')
    commits_by_repo, first_commit, last_commit = get_commits_by_repo(page['repos'], page['name'])

    data = {'style': get_css(CSS_FILE),
            'commits_by_repo': commits_by_repo,
            'first_commit': first_commit,
            'last_commit': last_commit,
            'rolling_paper': page['comments'],
            'name': page['name'], 'range': f'{first_commit["date"][:4]} ~ {last_commit["date"][:4]}'},

    with open(f'commit_book_{page["name"]}.html', 'w') as f:
        f.write(template.render(*data))
