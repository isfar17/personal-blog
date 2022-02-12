from distutils.log import error
from flask import render_template,Blueprint

error=Blueprint("error",__name__,template_folder="templates")

@error.app_errorhandler(404)
def error_404(e):
    return render_template("404.html"),404
    
@error.app_errorhandler(403)
def error_403(e):
    return render_template("403.html"),403

@error.app_errorhandler(500)
def error_403(e):
    return render_template("500.html"),500