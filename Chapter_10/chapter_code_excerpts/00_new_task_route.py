@app.route('/tasks/new', methods=['POST'])
def create_task():
    task = create_task_from_request(request.form)
    app.logger.info('Created task %s', task.id)  # Framework-specific logging
    return redirect(url_for('index'))
