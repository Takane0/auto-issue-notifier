from scanner import scan_files
import os

def write_temp_file(filename, lines):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def test_todo_detection():
    fname = 'test_todo.py'
    lines = ['print("Hello")', '# TODO check this', 'x = 2 # TODO']
    write_temp_file(fname, lines)
    matches = scan_files([fname], [], check_todo=True, check_merge=False)
    assert fname in matches
    assert len(matches[fname]) == 2
    os.remove(fname)

def test_merge_conflict_detection():
    fname = 'test_merge.py'
    lines = ['print("Safe")', '<<<<<<< HEAD', 'code1', '=======', '>>>>>>> branch']
    write_temp_file(fname, lines)
    matches = scan_files([fname], [], check_todo=False, check_merge=True)
    assert fname in matches
    assert len(matches[fname]) == 2
    os.remove(fname)

def test_no_detection():
    fname = 'test_clean.py'
    lines = ['print("Nothing here")', 'x = 22']
    write_temp_file(fname, lines)
    matches = scan_files([fname], [], check_todo=True, check_merge=True)
    assert fname not in matches
    os.remove(fname)

if __name__ == '__main__':
    test_todo_detection()
    test_merge_conflict_detection()
    test_no_detection()
    print("All tests passed.")
