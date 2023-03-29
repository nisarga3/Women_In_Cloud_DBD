from django.urls import path

from . import views

urlpatterns = [
    # ---- HOME ----
    path('', views.index),
    path('home', views.index),
    
    # ---- Login ----
    path("signin/",views.signin,name="default"),
    path('postsignin/',views.postsignin,name="postsignin"),
    path('logout/',views.logout,name="logout"),
    path("signup/",views.signup,name="signup"),
    path('postsignup/',views.postsignup,name="postsignup"),
    
    # ---- Login ----
    path("admin_index/",views.adview,name="adview"),    
    path("stud_index/",views.stview,name="stview"), 
    path("getstud/",views.getstud,name="getstud"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("power/",views.powerbi,name="dashboard"),

    # ---- Projects admin view----      
    path("projects/",views.projectview,name="projectview"),
    path("applied_students_projects/<int:project_id>/", views.applied_students_proj, name="applied_students_proj"),
    path("addproj/",views.addproj,name="addproj"),
    path("addproject/",views.addproject,name="addproject"),
    # ---- Projects student view----  
    path("hire_proj/<int:project_id>/<str:USN>/",views.hire_proj,name="hire_proj"),  #the stud view projects
    path("apply_projects/",views.stud_view_proj,name="stud_view_proj"),  #the stud view projects 
    path("applyproj/<int:project_id>/<str:USN>/",views.apply_proj,name="apply_proj"),  #the stud view projects 
    
     # ---- internships admin view----   
    path("internships/",views.internshipview,name="internshipview"),
    path("applied_students_internships/<int:internship_id>/", views.applied_students_intern, name="applied_students_intern"),
    path("addintern/",views.addintern,name="addintern"),
    path("addinternship/",views.addinternship,name="addinternship"),
    # ---- internships student view----  
    path("hire_intern/<int:internship_id>/<str:USN>/",views.hire_intern,name="hire_intern"),  #the stud view internships
    path("apply_internships/",views.stud_view_intern,name="stud_view_intern"),  #the stud view internships 
    path("applyintern/<int:internship_id>/<str:USN>/",views.apply_intern,name="apply_intern"),  #the stud view internships 

    # ---- events admin view----   
    path("events/",views.eventview,name="eventview"),
    path("applied_students_events/<int:event_id>/", views.applied_students_event, name="applied_students_event"),
    path("addevents/",views.addeve,name="addevents"),
    path("addevent/",views.addevent,name="addevent"),
    # ---- events student view----  
    path("apply_events/",views.stud_view_event,name="stud_view_event"),  #the stud view events 
    path("applyevent/<int:event_id>/<str:USN>/",views.apply_event,name="apply_event"),  #the stud view events 
    path("archivedeve/",views.archivedeve,name="archivedeve"),  #the stud view events 
    
    # ------fund-----
    path("addfund/",views.fund,name="addfund"),
    path("addfunds/",views.add_fund,name="addfunds"),
    path('int_download_csv/', views.intdownload_csv, name='intdownload_csv'),


]