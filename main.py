
from flask import Flask, render_template ,request
from flask_sqlalchemy import SQLAlchemy

from datetime import date
year = date.today().year

app=Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()

db.init_app(app)




filters=["🔌 Sockets","🚽 Toilet","🛜 Wifi","📱 Call"]
db_filters=["has_sockets","has_toilet","has_wifi","can_take_calls"]
user_filter=[]
result=[]
found_places=0

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=="GET":
        with app.app_context():
            cafe_table = db.Table('cafe', db.metadata, autoload_with=db.engine)
            cafes = db.session.query(cafe_table).all()
            result=cafes




    if request.method=="POST":

        pressed=list(request.form.keys())[0]
        print(type(list(request.form.values())[0]))
        with app.app_context():
            cafe_table = db.Table('cafe', db.metadata, autoload_with=db.engine)
            cafes = db.session.query(cafe_table).all()
            result = cafes
            if pressed in user_filter:
                user_filter.remove(pressed)

            else:

                user_filter.append(pressed)
            if len(user_filter)> 0:
                    result = []
                    for r in cafes:
                        for f in user_filter:
                            if user_filter[0] == f:
                                    found=r[6+user_filter.index(f)]
                                    if found:
                                        result.append(r)


                            else:

                                found = r[6 + user_filter.index(f)]
                                if not found:
                                    if r in result:
                                        result.remove(r)



                        result=list(set(result))
    found_places=len(result)







    return render_template("index.html",filters=filters,result=result,found_places=found_places,user_filter=user_filter,year=year)

if __name__ =="__main__":
    app.run(debug=True)
