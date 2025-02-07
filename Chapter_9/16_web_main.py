def main():
    """Create and run the Flask web application."""
    app_container = create_application(
        notification_service=NotificationRecorder(),
        task_presenter=WebTaskPresenter(),
        project_presenter=WebProjectPresenter(),
    )

    flask_app = create_web_app(app_container)
    flask_app.run(debug=True)


if __name__ == "__main__":
    main()
