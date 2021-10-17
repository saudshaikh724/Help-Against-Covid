from wtforms import Form, DateField

class TextForm(Form):
    #city = StringField('City',[validators.Length(min=5,max=25)])
    date = DateField()
