# randfpck: v1
> a refactored version of the randfpck cli app

## Actions taken

### Project structure

A new project structure has been laid out, with a `randfpck/` and `tests/` directory.

| NOTE: |
| :---- |
| The `tests/` directory need an `__init__.py` file, or the tests won't run. |

You can run the tests typing:

```bash
# run all tests showing only the summary
python -m unittest discover

# run all tests showing the individual tests executed (test functions)
python -m unittest discover -v
```

## ToDo

- [ ] Change the strategy of the logger definition.

    It was defined within the __main__ but it should be taken outside so that it is available everywheter.

- [ ] Create more files.

    Having everything in one humongous file doesn't make sense. Logger, file related operations, etc.