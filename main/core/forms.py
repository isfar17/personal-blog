from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length


class Contact(FlaskForm):
    feedback=TextAreaField(label="Feedback",validators=[DataRequired(message="Must provide Feedback!"),Length(1,2000)])
    submit=SubmitField("Submit")
