# Chapter 8: Test-Driven Clean Architecture: Ensuring Python Code Quality

The code exampes from the chapter can be found in the order of appearance in the files with numeric indexes (ex:
`00_error_class.py`)

## Companion task management application

This chapter explores how Clean Architecture's explicit boundaries and separation of concerns naturally enable comprehensive testing strategies. Using our task management system as an example, we'll see how Clean Architecture's structure supports different types of tests and makes testing more manageable and meaningful.


## Running the Tests

Ensure you have followed the instructions in the [Getting started](../README.md#2-getting-started) section to set up your environment.

Execute all tests using pytest:
```bash
cd Chapter_8/TodoApp
pytest
```

Run tests in parallel:
```bash
# ensure pytest-xdist is installed
pytest -n auto
```

Run tests in random order:
```bash
# ensure pytest-random-order is installed
pytest --random-order
```
