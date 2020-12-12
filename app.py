from flask import Flask, render_template, request, url_for,app
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField


app = Flask(__name__)

app.config["SECRET_KEY"] ="Looper23era" #VERY STRONG SECRET KEY
app.config["MONGO_URI"] = "mongodb+srv://test_user:Fewtrees789@learningmongodb.qfv7s.mongodb.net/db?retryWrites=true&w=majority"


mongo = PyMongo(app)

class Expenses(FlaskForm):
    # you need to complete the form for the following fields:
    # StringField for description
    description = StringField("Description")
    # SelectField for category
    category = SelectField("Category",choices=[('rent','rent'),
                                    ('electricity','electricity'),
                                    ('water','water'),
                                    ('gas','gas'),
                                    ('groceries','groceries'),
                                    ('insurance','insurance'),
                                    ('restaurants','restaurants'),
                                    ('college','college'),
                                    ('mortgage','mortgage'),
                                    ("party","party")])
    # DecimalField for cost
    cost = DecimalField("Cost")
    # DataField for date
    date = DateField("Date", format='%m/%d/%Y')


def get_total_expenses(category):
    # access the database adding the cost of all documents
    # of the category passed as input parameter
    # write the appropriate query to retrieve the cost
    category_query = {'category' : category}
    category_expense = mongo.db.expenses.find(category_query)
    total_cost = 0
    for i in category_expense:
        total_cost+=float(i["cost"])
    return total_cost

@app.route('/')
def index():
    my_expenses = mongo.db.expenses.find()
    total_cost = 0
    for i in my_expenses:
        total_cost+=float(i["cost"])
    total_cost_list = [total_cost]

    expensesByCatergory = [ #expense for cost of same catergory
        ("Rent = $" ,get_total_expenses("rent")),
        ("Electricity = $",get_total_expenses("electricity")),
        ("Water = $",get_total_expenses("water")),
        ("Insurance = $",get_total_expenses("insurance")),
        ("Restaurants = $",get_total_expenses("restaurants")),
        ("Groceries = $",get_total_expenses("groceries")),
        ("Gas = $",get_total_expenses("gas")),
        ("College = $",get_total_expenses("college")),
        ("Party = $",get_total_expenses("party")),
        ("Mortgage = $",get_total_expenses("mortgage"))
    ]
    return render_template("index.html",expenses=total_cost_list, expensesByCatergory=expensesByCatergory)



#page where expenses details can be entered and submitted
@app.route('/addExpenses',methods=["GET","POST"])
def addExpenses():
    expensesForm = Expenses(request.form)
    # INCLUDE THE FORM BASED ON class expenses
    if request.method == "POST":
        # INSERT ONE DOCUMENT TO THE DATABASE
        #CONTAINING THE DATA LOGGED BY THE USER
        #REMEMBER THAT IT SHOULD BE A PYTHON DICTIONARY
        description = request.form["description"]
        category = request.form["category"]
        cost = request.form["cost"]
        date = request.form["date"]
        expense_dict = [{'description': description, 'category' : category,
                         'cost' : cost, 'date' : date}]
        result = mongo.db.expenses.insert_one(expense_dict[0])
        # mongo.db.expenses.drop()
        return render_template("expenseAdded.html")
    return render_template("addExpenses.html", form=expensesForm)

app.run()


