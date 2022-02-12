from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class Register(FlaskForm):
    name=StringField(label="Name",validators=[DataRequired(message="Must provide name!"),Length(5,25)])
    email=StringField(label="Email",validators=[DataRequired(message="Must provide email!"),Email(),Length(8,45)])
    password=PasswordField(label="Password",validators=[DataRequired(message="Must provide password!"),EqualTo("retype_pass"),Length(8,75)])
    retype_pass=PasswordField(label="Retype-Password",validators=[DataRequired(message="Password must match!"),Length(8,75)])
    register=SubmitField("Register")

class Update_Profile(FlaskForm):
    name=StringField(label="Name",validators=[DataRequired(message="Must provide name!"),Length(5,25)])
    email=StringField(label="Email",validators=[DataRequired(message="Must provide email!"),Email(),Length(8,45)])
    update=SubmitField("Update")


class Login(FlaskForm):
    email=StringField(label="Email",validators=[DataRequired(message="Must provide email!"),Email(),Length(8,45)])
    password=PasswordField(label="Password",validators=[DataRequired(message="Must provide password!"),Length(8,75)])
    login=SubmitField("Login")

class PasswordChange(FlaskForm):
    password=PasswordField(label="Password",validators=[DataRequired(message="Must provide password!"),EqualTo("retype_pass"),Length(8,75)])
    retype_pass=PasswordField(label="Retype-Password",validators=[DataRequired(message="Password must match!"),Length(8,75)])
    change=SubmitField("Change")