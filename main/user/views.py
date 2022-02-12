
from flask import render_template,Blueprint,redirect,url_for,request,flash,abort
from .forms import Register,Login, Update_Profile,PasswordChange
from main.models import Blog, User
from main import db,login_manager
from flask_login import current_user, login_user,login_required, logout_user
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
user=Blueprint("user",__name__,template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@user.route("/login",methods=["GET","POST"])
def login():
    form=Login()
    if form.validate_on_submit():
        email=form.email.data
        query=User.query.filter_by(email=email).first()#grab the user corresponding to the given email
        if query!=None and query.check_password(form.password.data): #now check the password given by the user
            login_user(query)#if matches authenticate.this special method is imported form flask_login#show message
                        # flask saves that URL as 'next'.            
            next = request.args.get('next')#render next keyword from html request
            # So let's now check if that next exists,or the first string is "/"
            if next == None or next[0]!='/':
                next = url_for('core.home',page=1)#if not then go to default homepage or profile page
            flash(f"Howdy {query.name}!")
            return redirect(next)#
    return render_template("login.html",form=form)


@user.route("/logout")
@login_required
def logout():
    flash("You are logged out!")
    logout_user()
    return redirect(url_for("core.home",page=1))


@user.route("/register",methods=["GET","POST"])
def register():
    form=Register()
    if form.validate_on_submit():
        query1=User.query.filter_by(name=form.name.data).first()
        query2=User.query.filter_by(email=form.email.data).first()
        if query1 and not None:
            flash("This username has been taken!Please use another unique name")
            return redirect(url_for("user.register"))
        if query2 and not None:
            flash("This email has been taken!Please use another unique email")
            return redirect(url_for("user.register"))
        name=form.name.data
        email=form.email.data
        password=form.password.data
        user=User(name,email,password)
        db.session.add(user)
        db.session.commit()
        flash("Thanks For Signing Up!")
        return redirect(url_for("user.login"))

    return render_template("register.html",form=form)

@user.route("/user/<int:id>",methods=["GET","POST"])
@login_required
def profile(id):
    query=User.query.filter_by(id=id).first()
    if query is None:
        abort(404)
       # return redirect(url_for("core.home",page=1))
    return render_template("profile.html",query=query)



@user.route("/update_profile/<int:id>",methods=["GET","POST"])
@login_required
def update_profile(id):
    query=User.query.filter_by(id=id).first()
    if query is None:
        abort(403)
    if current_user.id!=query.id:
        abort(403)
    blog_author=Blog.query.filter_by(user_id=id).all()
    form=Update_Profile()
    if form.validate_on_submit():
        try:
            query.name=form.name.data
            for i in blog_author:
                i.created_by=query.name    
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This username has been taken! Please use another unique name")
            return redirect(url_for("user.update_profile",id=query.id))
        try:
            query.email=form.email.data
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This email has been taken! Please use another unique email")
            return redirect(url_for("user.update_profile",id=query.id))
        flash("Profile Updated")
        return redirect(url_for("user.profile",id=query.id))

    form.name.data=query.name
    form.email.data=query.email
    return render_template("update_profile.html",form=form,query=query)


@user.route("/delete_profile/<int:id>",methods=["GET","POST"])
@login_required
def delete_profile(id):
    query=User.query.filter_by(id=id).first()
    if query is None:
        abort(403)
    if current_user.id!=query.id:
        abort(403)
    blogs=Blog.query.filter_by(user_id=id).all()
    logout_user()
    for i in blogs:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(query)
    db.session.commit()
    flash("You are no longer a user of this website! Please create an account to join the community!")
    return redirect(url_for("core.home",page=1))

@user.route("/change_pass_user/<int:id>",methods=["GET","POST"])
def change_pass(id):
    query=User.query.filter_by(id=id).first()
    if query is None:
        abort(403)
    if current_user.id!=query.id:
        abort(403)
    form=PasswordChange()
    if form.validate_on_submit():
        query.password=generate_password_hash(form.password.data)
        db.session.commit()
        flash("Password changed successfully!")
        return redirect(url_for("user.profile",id=query.id))
    return render_template("change_pass.html",form=form,query=query)