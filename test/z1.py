from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

class Test_farP(db.Model):
    
    __tablename__ = 'Test_farP'

    ID = db.Column(db.String(90), primary_key=True)
    Start = db.Column(db.String(90))
    End = db.Column(db.String(90))
    SpN = db.Column(db.String(90))

    def __init__(self, ID, Start, End, SpN):
        self.ID = ID
        self.Start = Start
        self.End = End
        self.SpN = SpN
    

@app.route('/', methods=['post', 'get'])
def index():
    query = Test_farP.query.all()
    # sql_cmd = """
    #     select *
    #     from product
    #     """

    # query_data = db.engine.execute(sql_cmd)
    # print(query_data)
    # query = Test_farP.query.filter(Test_farP.ID.like("47387")).all()
    
    # return query.ID
    
    
    return render_template('mix.html',query=query)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    
    
    
    
    