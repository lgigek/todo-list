from routes.task_routes import app
from log import log_formatter

if __name__ == '__main__':
    app.run(host='0.0.0.0')
