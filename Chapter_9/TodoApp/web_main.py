"""
Entry point for the web interface of the Todo App.
"""

from todo_app.infrastructure.configuration.container import create_application
from todo_app.infrastructure.web.app import create_web_app
from todo_app.infrastructure.notifications.factory import create_notification_service
from todo_app.interfaces.presenters.web import WebProjectPresenter, WebTaskPresenter


def main():
    """Run the web interface."""
    notification_service = create_notification_service()
    task_presenter = WebTaskPresenter()
    project_presenter = WebProjectPresenter()

    app_container = create_application(
        notification_service=notification_service,
        task_presenter=task_presenter,
        project_presenter=project_presenter,
    )
    web_app = create_web_app(app_container)
    web_app.run(debug=True)


if __name__ == "__main__":
    main()
