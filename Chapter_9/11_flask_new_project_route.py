# todo_app/infrastructure/web/routes.py
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

        project = result.success
        flash(f'Project "{project.name}" created successfully', "success")
        return redirect(url_for("todo.index"))

    return render_template("project_form.html")
