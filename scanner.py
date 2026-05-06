import os
from pathlib import Path


def _make_context(lines, idx, radius=1):
    start = max(0, idx - radius)
    end = min(len(lines), idx + radius + 1)
    return ''.join(lines[start:end]).rstrip('\n')


def scan_files(include_patterns, exclude_dirs, check_todo=True, check_merge=True):
    # Find files to scan
    files = set()
    for pat in include_patterns:
        for match in Path('.').glob(pat):
            if match.is_file():
                files.add(str(match))

    exclude_dirs = set(exclude_dirs)
    results = {}
    for path in files:
        skip = False
        for ex in exclude_dirs:
            if ex and ex.rstrip('/') + '/' in path:
                skip = True
                break
        if skip or not os.path.isfile(path):
            continue

        with open(path, encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()

        issues = []
        for idx, line in enumerate(all_lines, 1):
            if check_todo and 'TODO' in line:
                issues.append({
                    'line': idx,
                    'match': 'TODO',
                    'context': _make_context(all_lines, idx - 1),
                })
            if check_merge and (line.strip().startswith('<<<<<<<') or line.strip().startswith('>>>>>>>')):
                issues.append({
                    'line': idx,
                    'match': 'merge conflict marker',
                    'context': _make_context(all_lines, idx - 1),
                })
        if issues:
            results[path] = issues
    return results
