# Clean Architecture with Python

This repository contains the companion application code for the book: "[Clean Architecture with Python](<link-to-book-if-available>)", published by Packt.

## Project Structure

The code is organized by chapter. Each `Chapter_X` folder (e.g., `Chapter_1`, `Chapter_2`) represents a progressive snapshot of the application's state at the end of that corresponding chapter in the book.

An example of the structure of a chapter folder is shown below:
- `README.md`: Contains instructions for running the application or tests for that chapter.
- `chapter_code_excerpts`: Contains the code snippets from the chapter in the order of appearance in the files with numeric indexes (ex: `00_error_class.py`). This is provided for reference and is not meant to be runnable.
- `TodoApp`: If applicable, contains the companion application code for that chapter. This code is runnable (to the extent of its implementation for the given chapter).

```
Chapter_4/
├── README.md
│
├── chapter_code_excerpts
│   ├── 00_create_new_task.py
│   ├── 01_create_task_business_rules.py
│   ├── 02_value_objects_in_clean_arch.py
│   ├── 03_project_usage.py
│   ├── ...
│
└── TodoApp
    └── todo_app
        ├── application
        ├── domain
        ├── infrastructure
        └── interfaces
```

All code has been tested and verified to work with Python 3.13 on MacOS and Windows.  With the nature of Python the code should work on other platforms that support a Python runtime, but this has not been verified.

## 1. Installing dependencies

### Dependency management

To simplify setup, this repository uses a single `pyproject.toml` file located at the root of the repository. This file defines the dependencies for the *entire* project, effectively installing the union of all packages required across all chapters.

We use [UV](https://docs.astral.sh/uv/) for managing dependencies. However, a `requirements.txt` file is also provided for users who prefer to use `pip` on its own.

### Installing dependencies with UV
If you have `uv` installed, you can use it to create the environment:

```shell
# Create the virtual environment
> uv venv

# Activate the environment
# On macOS/Linux:
> source .venv/bin/activate
# On Windows:
> .venv\Scripts\activate
```

Once your virtual environment is activated, install the required packages using one of the following methods:

```shell
# Sync dependencies using uv and pyproject.toml
> uv sync
```

### Installing dependencies with `pip`

**Creating a virtual environment:**

```shell
# Create the virtual environment
> python -m venv .venv

# Activate the environment
# On macOS/Linux:
> source .venv/bin/activate
# On Windows:
> .venv\Scripts\activate
```

**run `pip install`:**

```shell
# Ensure pip is up-to-date
> python -m pip install --upgrade pip

# Install dependencies using pip
> pip install -r requirements.txt
```

## 2. Explore and Run Chapter Code

Navigate to the specific chapter folder you're interested in. Each chapter has its own `README.md` file with instructions for running the application or tests for that chapter.

**Example: Running tests for Chapter 5**

```shell
# Navigate to the chapter's application folder
> cd Chapter_5/TodoApp

# Run tests (example command, may vary by chapter)
> pytest
```

---
