
from flask import render_template,Blueprint,url_for,redirect,abort,flash
from .forms import Update_Blog,Create_Blog
from flask_login import current_user, login_required
from main.models import Blog
from main import db
from datetime import datetime

blog=Blueprint("blog",__name__,template_folder="templates")

@blog.route("/create_blog",methods=["GET","POST"])
@login_required
def create_blog():
    form=Create_Blog()
    if form.validate_on_submit():
        time=datetime.utcnow()
        title=form.title.data
        content=form.content.data
        blog=Blog(title,content,user_id=current_user.id,created_by=current_user.name,time=time)
        db.session.add(blog)
        db.session.commit()
        flash("New post created!")
       # print(title,content,current_user.id,current_user.name)
        return redirect(url_for("core.home",page=1))
    return render_template("blog_create.html",form=form)

@blog.route("/<int:id>/update",methods=["GET","POST"])
@login_required
def update_blog(id):
    query=Blog.query.filter_by(id=id).first()
    if query is None:
        abort(403)
    if current_user.id!=query.user_id:
        abort(403)
    form=Update_Blog()
    if form.validate_on_submit():
        query.title=form.title.data
        query.content=form.content.data
        db.session.commit()
        return redirect(url_for("blog.blog_view",id=query.id))
    form.title.data=query.title
    form.content.data=query.content
    return render_template("blog_update.html",form=form,query=query)

@blog.route("/<int:id>/delete_blog",methods=["GET","POST"])
@login_required
def delete_blog(id):
    query=Blog.query.filter_by(id=id).first()
    if query is None:
        abort(403)
    if current_user.id!=query.user_id:
        abort(403)
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("core.home",page=1))

@blog.route("/blog/<int:id>",methods=["GET","POST"])
def blog_view(id):
    query=Blog.query.filter_by(id=id).first()
    if query is None:
        abort(404)
    return render_template("blog_view.html",query=query)