"""Run: PYTHONPATH=src python test_safe_name.py"""
from s3.s3_crud import safe_name

assert safe_name("poza.png") == "poza.png"
assert safe_name("../../src/main.py") == "main.py"
assert safe_name("..\\..\\main.py") == "main.py"
assert safe_name("/etc/passwd") == "passwd"
for bad in ("", "..", ".", "../", None):
    try:
        safe_name(bad)
        raise AssertionError(f"accepted {bad!r}")
    except ValueError:
        pass
print("ok")
