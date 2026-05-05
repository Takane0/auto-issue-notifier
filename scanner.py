import os
glob_has = False
try:
    from glob import glob
    glob_has = True
except ImportError:
    glob_has = False

def scan_files(include_patterns, exclude_dirs, check_todo=True, check_merge=True):
    # Find files to scan
    files = set()
    if glob_has:
        import glob
        for pat in include_patterns:
            files.update(glob.glob(pat, recursive=True))
    else:
        # If glob not available, scan all py files in cwd
        for fname in os.listdir('.'):
            if fname.endswith('.py'):
                files.add(fname)
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
            issues = []
            for idx, line in enumerate(f, 1):
                if check_todo and 'TODO' in line:
                    issues.append({'line': idx, 'match': 'TODO'})
                if check_merge and (line.strip().startswith('<<<<<<<') or line.strip().startswith('>>>>>>>')):
                    issues.append({'line': idx, 'match': 'merge conflict marker'})
            if issues:
                results[path] = issues
    return results
