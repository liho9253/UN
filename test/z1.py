from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
db.init_app(app)

class Model(db.Model):
    
    __tablename__ = 'Test_farP'

    id = db.Column(db.Integer, primary_key=True)
    ID = db.Column(db.String(90))
    Start = db.Column(db.String(90))
    End = db.Column(db.String(90))
    SpN = db.Column(db.String(90))

    def __init__(self, ID, Start, End, SpN):
        self.ID = ID
        self.Start = Start
        self.End = End
        self.SpN = SpN

    

@app.route('/')
def index():

    sql_cmd = """
        select *
        from product
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    
    
    
    
    