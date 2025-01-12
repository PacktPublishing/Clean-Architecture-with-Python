class Config:
    @classmethod
    def get_repository_type(cls) -> RepositoryType:
        repo_type_str = os.getenv("TODO_REPOSITORY_TYPE", cls.DEFAULT_REPOSITORY_TYPE.value)
        try:
            return RepositoryType(repo_type_str.lower())
        except ValueError:
            raise ValueError(f"Invalid repository type: {repo_type_str}")


# A factory function to create repositories
def create_repositories() -> Tuple[TaskRepository, ProjectRepository]:
    repo_type = Config.get_repository_type()
    if repo_type == RepositoryType.FILE:
        data_dir = Config.get_data_directory()
        task_repo = FileTaskRepository(data_dir)
        project_repo = FileProjectRepository(data_dir)
        project_repo.set_task_repository(task_repo)
        return task_repo, project_repo
    elif repo_type == RepositoryType.MEMORY:
        task_repo = InMemoryTaskRepository()
        project_repo = InMemoryProjectRepository()
        project_repo.set_task_repository(task_repo)
        return task_repo, project_repo
    else:
        raise ValueError(f"Invalid repository type: {repo_type}")
