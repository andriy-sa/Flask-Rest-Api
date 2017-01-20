from app import app
from views.default import default_view
from views.users import users_view
from views.companies import companies_view

# Register Routes
app.register_blueprint(users_view, url_prefix='/api/user')
app.register_blueprint(companies_view, url_prefix='/api/company')
# must register last one
app.register_blueprint(default_view)

if __name__ == "__main__":
    app.run()