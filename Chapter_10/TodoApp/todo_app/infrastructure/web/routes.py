"""
Flask routes for the Todo App.
"""

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from todo_app.domain.value_objects import Priority
from todo_app.interfaces.presenters.web import WebProjectPresenter, WebTaskPresenter

bp = Blueprint("todo", __name__)
project_presenter = WebProjectPresenter()
task_presenter = WebTaskPresenter()


@bp.route("/")
def index():
    """List all projects with their tasks."""
    app = current_app.config["APP_CONTAINER"]
    show_completed = request.args.get("show_completed", "false").lower() == "true"

    result = app.project_controller.handle_list()
    if not result.is_success:
        error = project_presenter.present_error(result.error.message)
        flash(error.message, "error")
        return redirect(url_for("todo.index"))

    return render_template("index.html", projects=result.success, show_completed=show_completed)


@bp.route("/projects/new", methods=["GET", "POST"])
def new_project():
    """Create a new project."""
    if request.method == "POST":
        name = request.form["name"]
        app = current_app.config["APP_CONTAINER"]
        result = app.project_controller.handle_create(name)

        if not result.is_success:
            error = project_presenter.present_error(result.error.message)
            flash(error.message, "error")
            return redirect(url_for("todo.index"))

        # Use view model directly from controller response
        project = result.success
        flash(f'Project "{project.name}" created successfully', "success")
        return redirect(url_for("todo.index"))

    return render_template("project_form.html")


@bp.route("/projects/<project_id>/task  s/new", methods=["GET", "POST"])
def new_task(project_id):
    """Create a new task in a project."""
    if request.method == "POST":
        app = current_app.config["APP_CONTAINER"]
        result = app.task_controller.handle_create(
            project_id=project_id,
            title=request.form["title"],
            description=request.form["description"],
            priority=request.form["priority"],
            due_date=request.form["due_date"] if request.form["due_date"] else None,
        )

        if not result.is_success:
            error = task_presenter.present_error(result.error.message)
            flash(error.message, "error")
            return redirect(url_for("todo.index"))

        # Use view model directly from controller response
        task = result.success
        flash(f'Task "{task.title}" created successfully', "success")
        return redirect(url_for("todo.index"))

    return render_template("task_form.html", project_id=project_id)


@bp.route("/tasks/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """Edit an existing task."""
    app = current_app.config["APP_CONTAINER"]

    if request.method == "POST":
        # Handle empty due date - if the field is empty or just whitespace, set to empty string
        # This ensures UpdateTaskRequest gets an empty string which it will convert to None
        due_date = request.form.get("due_date", "").strip()

        result = app.task_controller.handle_update(
            task_id=task_id,
            title=request.form["title"],
            description=request.form["description"],
            priority=request.form["priority"],
            due_date=due_date,
        )

        if not result.is_success:
            error = task_presenter.present_error(result.error.message)
            flash(error.message, "error")
            return redirect(url_for("todo.edit_task", task_id=task_id))

        flash("Task updated successfully!", "success")
        return redirect(url_for("todo.index"))

    result = app.task_controller.handle_get(task_id)
    if not result.is_success:
        error = task_presenter.present_error(result.error.message)
        flash(error.message, "error")
        return redirect(url_for("todo.index"))

    return render_template("edit_task.html", task=result.success)


@bp.route("/tasks/<task_id>/complete", methods=["POST"])
def complete_task(task_id):
    """Complete a task."""
    app = current_app.config["APP_CONTAINER"]

    # Complete the task with optional notes
    result = app.task_controller.handle_complete(
        task_id=task_id, notes=request.form.get("completion_notes")
    )

    if not result.is_success:
        error = task_presenter.present_error(result.error.message)
        flash(error.message, "error")
    else:
        task = result.success
        flash(f'"{task.title}" marked as complete', "success")

    return redirect(
        url_for("todo.index", show_completed=request.args.get("show_completed", "false"))
    )
