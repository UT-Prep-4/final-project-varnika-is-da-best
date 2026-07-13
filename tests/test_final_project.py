import ast
import sys
from pathlib import Path

# The final project is open-ended and may block on input(), loop forever, or open
# a window, so this grader (like the mini-project's) NEVER runs your code. It reads
# every .py file in the repo with `ast` and checks the showcase-worthiness basics:
# organized into functions, real logic, substantial size, and a filled-out PROJECT.md.
# Whether the project is impressive and demo-ready is judged by humans at showcase!

MAIN_FILE = 'final_project.py'
SKIP_DIRS = {'tests', '.git', '.devcontainer', '.github', '__pycache__'}

def _project_files():
    files = []
    for path in Path('.').rglob('*.py'):
        if not any(part in SKIP_DIRS for part in path.parts):
            files.append(path)
    return files

def _trees():
    trees = []
    for path in _project_files():
        with open(path, encoding='utf-8') as f:
            trees.append((path, ast.parse(f.read(), filename=str(path))))
    return trees

def test_files_parse():
    assert Path(MAIN_FILE).exists(), "final_project.py is missing — that's the entry point!"
    try:
        _trees()
    except SyntaxError as e:
        assert False, f"{e.filename} has a syntax error on line {e.lineno}: {e.msg}"

def test_organized_code():
    # "Segments" can be functions, classes, or separate .py files — any of these
    # counts as organizing your code instead of one giant blob.
    trees = _trees()
    functions = sum(len([n for n in ast.walk(t) if isinstance(n, ast.FunctionDef)]) for _, t in trees)
    classes = sum(len([n for n in ast.walk(t) if isinstance(n, ast.ClassDef)]) for _, t in trees)
    files = len(trees)
    assert functions >= 3 or classes >= 1 or files >= 2, (
        "Showcase-worthy code is organized into clear segments, not one giant blob: "
        "use 3+ functions, a class, or split into multiple .py files "
        f"(found {functions} functions, {classes} classes, {files} file(s))."
    )

def test_has_real_logic():
    ifs = loops = 0
    for _, tree in _trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                ifs += 1
            if isinstance(node, (ast.For, ast.While)):
                loops += 1
    assert ifs >= 1 and loops >= 1, (
        "Your project needs real logic: decisions (if/elif/else) AND repetition "
        f"(for/while) working together (found {ifs} ifs, {loops} loops)."
    )

def test_substantial_project():
    count = sum(
        len([n for n in ast.walk(tree) if isinstance(n, ast.stmt)])
        for _, tree in _trees()
    )
    assert count >= 40, (
        "This is the FINAL project — it should be a multi-day build, bigger than "
        f"the mini-project (found {count} statements; aim well past 40)."
    )

def test_project_writeup():
    path = Path('PROJECT.md')
    assert path.exists(), "PROJECT.md is missing — showcase projects need a write-up!"
    content = path.read_text(encoding='utf-8')
    assert 'REPLACE THIS' not in content, (
        "PROJECT.md still has 'REPLACE THIS' placeholders — fill in every section "
        "so a stranger could understand and run your project."
    )
    assert len(content) >= 300, (
        "PROJECT.md is too short — write it like the resume entry it will become."
    )

if __name__ == '__main__':
    tests = [
        test_files_parse,
        test_organized_code,
        test_has_real_logic,
        test_substantial_project,
        test_project_writeup,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  ✅ PASSED: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ FAILED: {test.__name__} — {e}")

    print(f"\n{passed}/{len(tests)} checks passed.")
    if passed < len(tests):
        sys.exit(1)  # Causes the Action to show as failed in GitHub
