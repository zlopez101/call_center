from ut import create_app
from ut.config import Config

app = create_app(config_class=Config)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
