"""TimeCheck Root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from activities.views import GroupActivityViewSet, HomeActivityViewSet
from groups.views import GroupViewSet, AcceptInviteView, InviteGroupView
from polls.views import PollViewSet
from notes.views import NoteViewSet

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(
    r'activity',
    HomeActivityViewSet,
    basename='activity'
)
group_routes = router.register(
    r'group',
    GroupViewSet,
    basename='group',
)
group_routes.register(
    r'activity',
    GroupActivityViewSet,
    basename='activity',
    parents_query_lookups=('group',),
)
group_routes.register(
    r'poll',
    PollViewSet,
    basename='poll',
    parents_query_lookups=('group',),
)
group_routes.register(
    r'note',
    NoteViewSet,
    basename='note',
    parents_query_lookups=('group',),
)

urlpatterns = [
    path('user/', include('users.urls')),
    path('invite/<str:invite>/accept', AcceptInviteView.as_view(), name='accept_invite'),
    path('invite/<str:invite>/group', InviteGroupView.as_view(), name='invite_details'),
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
