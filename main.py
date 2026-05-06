import os
import sys
import yaml
from scanner import scan_files
from github_api import create_or_update_issue

CONFIG_PATH = 'config.yaml'


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def format_issue_body(matches):
    body_lines = ['The following code problems were found:\n']
    for fname, issues in matches.items():
        for issue in issues:
            line_no = issue['line']
            match_text = issue.get('match', 'issue found')
            body_lines.append(f"- {fname}: line {line_no} — {match_text}")
            snippet = issue.get('context') or issue.get('snippet')
            if snippet:
                body_lines.append('```')
                body_lines.extend(snippet.splitlines())
                body_lines.append('```')
    return '\n'.join(body_lines)


def main():
    config = load_config()
    github_repo = config['github']['repo']
    github_token = os.environ.get('GITHUB_TOKEN', config['github'].get('token', ''))
    issue_title = config['github'].get('issue_title', 'Possible TODOs or Merge Conflicts Detected')

    if not github_repo or not github_token:
        print("Please set your GitHub repo and token in config.yaml or as the GITHUB_TOKEN env variable.")
        sys.exit(1)

    matches = scan_files(
        include_patterns=config.get('include_files', ['**/*.py']),
        exclude_dirs=config.get('exclude_dirs', []),
        check_todo=config['checks'].get('todo', True),
        check_merge=config['checks'].get('merge_conflict', True)
    )

    if matches:
        issue_body = format_issue_body(matches)
        create_or_update_issue(github_repo, github_token, issue_title, issue_body)
        print("GitHub issue created/updated.")
    else:
        print("No issues found.")


if __name__ == '__main__':
    main()
