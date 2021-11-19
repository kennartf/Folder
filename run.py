from web_app import db
from web_app import app




if __name__ == "__main__":
    db.create_all()
    app.run(debug=False)
    
