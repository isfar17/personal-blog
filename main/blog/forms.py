from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length

class Create_Blog(FlaskForm):
    title=TextAreaField("Title",validators=[DataRequired("Must provide Title!"),Length(1,300)])
    content=TextAreaField("Content",validators=[DataRequired("Must provide Content!"),Length(1,3000)])
    create=SubmitField("Create")
 
 
class Update_Blog(FlaskForm):
    title=TextAreaField("Title",validators=[DataRequired("Must provide Title!"),Length(1,300)])
    content=TextAreaField("Content",validators=[DataRequired("Must provide Content!"),Length(1,3000)])
    submit=SubmitField("Submit")