<h1 align="center">
Clean Architecture with Python, First Edition</h1>
<p align="center">This is the code repository for <a href ="https://www.packtpub.com/en-us/product/clean-architecture-with-python-9781836642893"> Clean Architecture with Python, First Edition</a>, published by Packt.
</p>

<h2 align="center">
Implement scalable and maintainable applications using proven architectural principles
</h2>
<p align="center">
Sam Keen</p>

<p align="center">
  <a href="https://packt.link/free-ebook/9781836642893"><img width="32px" alt="Free PDF" title="Free PDF" src="https://cdn-icons-png.flaticon.com/512/4726/4726010.png"/></a>
 &#8287;&#8287;&#8287;&#8287;&#8287;
  <a href="https://packt.link/gbp/9781836642893"><img width="32px" alt="Graphic Bundle" title="Graphic Bundle" src="https://cdn-icons-png.flaticon.com/512/2659/2659360.png"/></a>
  &#8287;&#8287;&#8287;&#8287;&#8287;
   <a href="https://www.amazon.com/Clean-Architecture-Python-maintainable-architectural/dp/183664289X/ref=sr_1_1?dib=eyJ2IjoiMSJ9.mrQl3brdTItmT4A6S_fMXlsy29dfMx1L04R51_jgS-uHcAg8Yh-l_QyiemSeaVm18Q2YxMNcvDL9WRg9qf9yuf73T4PJdvZH9a9ZyDIjRaiRLRWH5V6NvUadxhAB6uLLDSUAYTHcXeCZEpE5PniWr9DN6bd0AOxolvVJ2iu-xAmG1KtekG2bUbtAwyOk7BLkdbj4xdnCemIdOW_b8Z6nuyAvfsfYW3OgEXudWjWf6fc.kN48Oi3kYx3L5-ybldBU546YRu9O8Hq4EgztLaiXkG0&dib_tag=se&keywords=Clean+Architecture+with+Python&qid=1750662628&sr=8-1"><img width="32px" alt="Amazon" title="Get your copy" src="https://cdn-icons-png.flaticon.com/512/15466/15466027.png"/></a>
  &#8287;&#8287;&#8287;&#8287;&#8287;
</p>
<details open> 
  <summary><h2>About the book</summary>
<a href="https://www.packtpub.com/en-us/product/clean-architecture-with-python-9781836642893">
<img src="https://content.packt.com/B31577/cover_image_small.jpg" alt="Clean Architecture with Python" height="256px" align="right">
</a>

In the rapidly evolving tech industry, software applications struggle to keep pace with changing business needs, leaving developers grappling with complex codebases that resist change, ultimately reducing productivity and increasing technical debt. Clean Architecture with Python offers a powerful approach to address these challenges. Drawing from his extensive experience architecting cloud-native systems, Sam Keen helps you transform complex architectural challenges into digestible, implementable solutions.
This book teaches essential principles for effective development, emphasizing the Pythonic implementation of Clean Architecture. Through practical examples, you'll learn how to create modular, loosely coupled systems that are easy to understand, modify, and extend. The book covers key concepts such as the Dependency Rule, separation of concerns, and domain modeling, all tailored for Python development.
By the end of this book, you'll be able to apply Clean Architecture principles effectively in your Python projects. Whether you're building new systems or managing existing ones, you'll have the skills to create more maintainable and adaptable applications. This approach will enhance your ability to respond to changing requirements, setting you up for long-term success in your development career.</details>
<details open> 
  <summary><h2>Key Learnings</summary>
<ul>

<li>Apply Clean Architecture principles idiomatically in Python</li>

<li>Implement domain-driven design to isolate core business logic</li>

<li>Apply SOLID principles in a Pythonic context to improve code quality</li>

<li>Structure projects for maintainability and ease of modification</li>

<li>Develop testing techniques for cleanly architected Python applications</li>

<li>Refactor legacy Python code to adhere to Clean Architecture principles</li>

<li>Design scalable APIs and web applications using Clean Architecture</li>

</ul>

  </details>

<details open> 
  <summary><h2>Chapters</summary>
     <img src="https://cliply.co/wp-content/uploads/2020/02/372002150_DOCUMENTS_400px.gif" alt="Clean Architecture with Python" height="436px" align="right">
<ol>

  <li>Clean Architecture Essentials: Transforming Python Development</li>

  <li>SOLID Foundations: Building Robust Python Applications</li>

  <li>Type-Enhanced Python: Strengthening Clean Architecture</li>

  <li>Domain-Driven Design: Crafting the Core Business Logic</li>

  <li>The Application Layer: Orchestrating Use Cases</li>

  <li>The Interface Adapters Layer: Controllers and Presenters</li>

  <li>The Frameworks and Drivers Layer: External Interfaces</li>

  <li>Implementing Test Patterns with Clean Architecture</li>

  <li>Adding Web UI: Clean Architecture's Interface Flexibility</li>

  <li>Implementing Clean Architecture Observability: Monitoring and Verification</li>

  <li>Legacy to Clean: Refactoring Python for Maintainability</li>

  <li>Your Clean Architecture Journey: Next Steps</li>

</ol>

</details>


<details open> 
  <summary><h2>Project Structure</summary>
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

  </details>
<details open> 
  <summary><h2>1. Installing dependencies</summary>

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
  </details>
<details open> 
  <summary><h2>2. Explore and Run Chapter Code</summary>
Navigate to the specific chapter folder you're interested in. Each chapter has its own `README.md` file with instructions for running the application or tests for that chapter.

**Example: Running tests for Chapter 5**

```shell
# Navigate to the chapter's application folder
> cd Chapter_5/TodoApp

# Run tests (example command, may vary by chapter)
> pytest
```
  </details>

<details> 
  <summary><h2>Get to know Authors</h2></summary>

_Sam Keen_ Sam Keen is a software engineering leader with over 25 years of experience. A polyglot developer who's leveraged Python in varied contexts from small startups to industry giants including AWS, Lululemon, and Nike. His expertise spans cloud architecture, continuous delivery, and building scalable systems. At Lululemon, Sam pioneered the company's first cloud-native software development team, setting standards for distributed cloud architecture within the company. Currently, Sam leverages Python to design and implement internal platform engineering solutions for AWS focusing on clean architecture principles and maintainable code. Sam resides in the US Pacific Northwest with his wife and two cats.

</details>
<details> 
  <summary><h2>Other Related Books</h2></summary>
<ul>

  <li><a href="https://www.packtpub.com/en-us/product/learn-python-programming-9781835882948">Learn Python Programming, Fourth Edition</a></li>

  <li><a href="https://www.packtpub.com/en-us/product/clean-code-in-python-9781800560215">Clean Code in Python, Second Edition</a></li>

  <li><a href="https://www.packtpub.com/en-us/product/python-object-oriented-programming-9781801077262">Python Object-Oriented Programming, Fourth Edition</a></li>
 
</ul>

</details>
