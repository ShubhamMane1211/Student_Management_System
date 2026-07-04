from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from services.dashboard_service import DashboardService

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def dashboard():

    return render_template(
        "dashboard/dashboard.html",
        total_students=DashboardService.total_students(),
        total_subjects=DashboardService.total_subjects(),
        total_marks=DashboardService.total_marks(),
        average_marks=DashboardService.average_marks(),
        highest_marks=DashboardService.highest_marks(),
        lowest_marks=DashboardService.lowest_marks(),
        top_students=DashboardService.top_students(),
        subject_statistics=DashboardService.subject_statistics(),
        recent_marks=DashboardService.recent_marks(),
        grade_distribution=DashboardService.grade_distribution(),
        recent_students=DashboardService.recent_students(),
    )


@main.route("/api/dashboard/grade-distribution")
@login_required
def grade_distribution_api():

    return jsonify(DashboardService.grade_distribution())


@main.route("/api/dashboard/subject-statistics")
@login_required
def subject_statistics_api():

    data = DashboardService.subject_statistics()

    return jsonify(
        [{"subject": subject, "average": round(avg, 2)} for subject, avg in data]
    )
