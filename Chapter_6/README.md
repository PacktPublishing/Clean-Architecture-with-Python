# Chapter 6

The code from the chapter can be found in the order of appearance in the files with numeric indexes (ex:
`00_error_class.py`)

In addition to that the evolving personal todo app files aligned with the chapter content can be found in the `ToDoApp`
folder.

**Note:** You will see a `infrastructure` folder also.  This is not part of the chapter 6 content, only there to support the development of the interfaces code.  The full development of the infrastructure code, (Framework/Drivers layer), is covered in chapter 7.

```text
└── todo_app
    ├── application
    │    ├── common
    │    │    └── result.py
    │    ├── dtos
    │    │    ├── project_dtos.py
    │    │    └── task_dtos.py
    │    ├── ports
    │    │    └── notifications.py
    │    ├── repositories
    │    │    ├── project_repository.py
    │    │    └── task_repository.py
    │    └── use_cases
    │        ├── project_use_cases.py
    │        └── task_use_cases.py
    └── domain
    │   ├── entities
    │   │    ├── entity.py
    │   │    ├── project.py
    │   │    └── task.py
    │   ├── exceptions.py
    │   ├── services
    │   │    └── task_priority_calculator.py
    │   └── value_objects.py
    │
    └── interface   
        ├── controllers  
        │   ├── project_controller.py
        │   └── task_controller.py
        ├── presenters
        │   ├── base.py
        │   └── cli.py
        └── view_models
            ├── base.py
            ├── project_vm.py
            └── task_vm.py
```