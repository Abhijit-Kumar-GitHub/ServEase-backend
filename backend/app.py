from flask import Flask
from routes.consumer_routes import consumer_bp
from routes.service_provider_routes import service_provider_bp

app = Flask(__name__)

        

# Register consumer routes
app.register_blueprint(consumer_bp, url_prefix='/consumer')
# Register consumer service- providers routes
app.register_blueprint(service_provider_bp, url_prefix='/service_provider')



if __name__ == '__main__':
    app.run(debug=True)
