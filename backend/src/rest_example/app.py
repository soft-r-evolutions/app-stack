import connexion
from db import Db

db = Db()

# Create the application instance
app = connexion.App(__name__, specification_dir='../swaggers')

app.add_api("swagger.yml")


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

