# from flask import Blueprint, render_template
# from flask_login import login_required

# from services.dashboard_service import DashboardService

# dashboard = Blueprint(
#     "dashboard",
#     __name__,
#     url_prefix="/dashboard"
# )


# @dashboard.route("/")
# @login_required
# def home():

#     return render_template(
#         "dashboard/dashboard.html",

#         total_students=DashboardService.total_students(),

#         total_subjects=DashboardService.total_subjects(),

#         total_marks=DashboardService.total_marks(),

#         average_marks=DashboardService.average_marks(),

#         highest_marks=DashboardService.highest_marks(),

#         lowest_marks=DashboardService.lowest_marks(),

#         top_students=DashboardService.top_students()
#     )