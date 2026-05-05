import requests

def create_or_update_issue(repo, token, title, body):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
    }
    # Get open issues
    issues_url = f'https://api.github.com/repos/{repo}/issues'
    q = {'state': 'open', 'per_page': 100}
    resp = requests.get(issues_url, headers=headers, params=q)
    resp.raise_for_status()
    existing = [i for i in resp.json() if i.get('title') == title]

    if existing:
        number = existing[0]['number']
        update_url = f'{issues_url}/{number}'
        patch = {'body': body}
        requests.patch(update_url, headers=headers, json=patch)
    else:
        data = {
            'title': title,
            'body': body,
        }
        requests.post(issues_url, headers=headers, json=data)
