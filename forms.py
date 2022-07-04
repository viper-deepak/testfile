from flask_wtf import Form
from wtforms import  IntegerField, RadioField,SubmitField
from wtforms import validators

class TransactionForm(Form):
   ttype = RadioField('Transaction Type', choices = [('Credit','Deposit'),('Debit','Withdrawl')])
   amount = IntegerField("Amount")
   submit = SubmitField("Confirm")

