# Hello, using fakes and doubles in PyTest
> illustrates how to use fakes and doubles in PyTest

## To run the tests

```bash
# Run the tests auto-discovering the test
pytest
=================================== test session starts ====================================
platform linux -- Python 3.10.13, pytest-8.0.2, pluggy-1.4.0
rootdir: /home/ubuntu/Development/git-repos/side_projects/python-workbench/part_4-web-apps/part-ii-fastapi-in-depth/10_fastapi-testing/01_hello-pytest-mocking
collected 1 item
```

To run the test in quiet mode:

```bash
$ pytest -q
.                                                                                    [100%]
1 passed in 0.01s
```

To run a specific test file:

```bash
$ pytest -q tests/unit/test_summer1.py
.                                                                                                                                                                                                                             [100%]
1 passed in 0.01s
```

## Troubleshooting

Sometimes you'll get errors similar to "Module not found" when executing `pytest` from the command line, while everything works from the Testing icon in vscode.

In those cases, delete the virtual environment and then run `poetry install` again.