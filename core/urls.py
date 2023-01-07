from django.urls import path
from .views import Authentication, Dashboard

urlpatterns = [
    path('', Dashboard.index, name='dashboard'),
    path('signup', Authentication.signup, name='signup'),
    path('login', Authentication.loginuser, name='loginuser'),
    path('logout', Authentication.logoutuser, name='logoutuser'),
    path('category/<int:id>', Dashboard.category, name='category'),
    path('alltasks', Dashboard.alltasks, name='alltasks'),
    path('important', Dashboard.importanttasks, name='importanttasks'),
    path('taskcheck/<int:id>/<int:categoryid>', Dashboard.taskcheck, name='taskcheck'),
    path('completedtasks', Dashboard.completedtasks, name='completedtasks'),
    path('addtask/<int:categoryid>', Dashboard.addtask, name='addtask'),
    path('deletetask/<int:id>/<int:categoryid>', Dashboard.deletetask, name='deletetask'),
    path('importance/<int:id>/<int:categoryid>', Dashboard.importance, name='importance'),
    
]
