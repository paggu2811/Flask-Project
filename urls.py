from main import app
import category_operation as cat
import song_operation as sn
import admin
import user

############  Category #################
app.add_url_rule("/addCategory1", view_func=cat.addCategory1, methods=["GET", "POST"])
app.add_url_rule("/showAllCategory1", view_func=cat.showAllCategory1)
app.add_url_rule("/deleteCategory1/<cid>", view_func=cat.deleteCategory1, methods=["GET", "POST"])
app.add_url_rule("/editCategory1/<cid>", view_func=cat.editCategory1, methods=["GET", "POST"])

############# Song ##############
app.add_url_rule("/addsong", view_func=sn.addsong, methods=["GET", "POST"])
app.add_url_rule("/showAllsong", view_func=sn.showAllsong)

############### Admin #######################
app.add_url_rule("/adminLogin", view_func=admin.adminlogin, methods=["GET", "POST"])
app.add_url_rule("/adminDashboard", view_func=admin.adminDashboard)

################# User #####################
app.add_url_rule("/", view_func=user.homepage)
app.add_url_rule("/ViewSongs/<cid>", view_func=user.ViewSongs)
app.add_url_rule("/ViewDetails/<song_id>", view_func=user.ViewDetails, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=user.login, methods=["GET", "POST"])
app.add_url_rule("/signup", view_func=user.signup, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=user.logout)   # ✅ GET only is enough
app.add_url_rule("/Playlist", view_func=user.showplaylist, methods=["GET", "POST"])  # ✅ lowercase
app.add_url_rule("/payment", view_func=user.payment, methods=["GET", "POST"])
