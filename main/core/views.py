from flask_login import current_user, login_required
from main import db
from flask import render_template,Blueprint,flash,abort,redirect,url_for
from main.core.forms import Contact
from main.models import Blog,Feedback, User

core=Blueprint("core",__name__,template_folder="templates")

@core.route("/")
def index():
    query=Blog.query.filter_by().order_by(Blog.time.desc()).paginate(per_page=5,page=1,error_out=False)
    return render_template("home.html",query=query)
@core.route("/<int:page>")
def home(page):
    query=Blog.query.filter_by().order_by(Blog.time.desc()).paginate(per_page=5,page=page,error_out=False)
    return render_template("home.html",query=query)

@core.route("/feedback",methods=["GET","POST"])
@login_required
def feedback():
    query=User.query.filter_by(email=current_user.email).first()
    form=Contact()
    if form.validate_on_submit():      
        email=query.email
        feedback=form.feedback.data
        info=Feedback(email,feedback)
        #print(email,feedback)
        db.session.add(info)
        db.session.commit()
        flash("Thanks for your feedback!")
        return redirect(url_for("core.home",page=1))
    return render_template("feedback.html",form=form,query=query)

@core.route("/about")
def about():
    return render_template("about.html")