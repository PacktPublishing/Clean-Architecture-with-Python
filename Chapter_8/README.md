# Chapter 8: Test-Driven Clean Architecture: Ensuring Python Code Quality

## Chapter code excerpts
The code snippets from the chapter can be found in the order of appearance in the `chapter_code_excerpts` folder. Examples: `00_error_class.py`  
These are provided for reference and are not meant to be runnable.

## Companion task management application

This chapter explores how Clean Architecture's explicit boundaries and separation of concerns naturally enable comprehensive testing strategies. Using our task management system as an example, we'll see how Clean Architecture's structure supports different types of tests and makes testing more manageable and meaningful.


## Running the Tests

Ensure you have followed the instructions in the repository's [README](../README.md) section to set up your environment.

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
