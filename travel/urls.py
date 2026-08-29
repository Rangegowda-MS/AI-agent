from django.urls import include, path

from .views import (
    home,
    planner,
    admin_login,
    admin_logout,
    admin_dashboard,
    admin_trip_detail,
)


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        home,
        name="home",
    ),

    # =====================================================
    # AI PLANNER
    # =====================================================

    path(
        "planner/",
        planner,
        name="planner",
    ),

    # =====================================================
    # ADMIN LOGIN
    # =====================================================

    path(
        "admin-login/",
        admin_login,
        name="admin_login",
    ),

    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard",
    ),

    # =====================================================
    # ADMIN TRIP DETAIL
    # =====================================================

    path(
        "admin-trip/<int:trip_id>/",
        admin_trip_detail,
        name="admin_trip_detail",
    ),

    # =====================================================
    # ADMIN LOGOUT
    # =====================================================

    path(
        "admin-logout/",
        admin_logout,
        name="admin_logout",
    ),

    # =====================================================
    # AI API
    # =====================================================

    path(
        "api/",
        include("travel.api_urls"),
    ),
]