"""The terminal output vocabulary shared by stdlib-only python command-line tools.

Only `ui` and `colors` leave this repository, and they leave as copies: each tool must
run on a machine that has nothing but `python3`, so none of them can install a package.
"""
