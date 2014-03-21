from django.conf.urls import url, patterns

from amway_customer_service.restful_api.sr_restful import SRUserSignupView, SRUserFollowUpView, SRUserAddFollowUpView, SRUserDeleteFollowUpView, \
    SRUserUpdateFollowUpView


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'amway_customer_service.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^api/sr/signup/', SRUserSignupView.as_view()),
                       url(r'^api/sr/(\d+)/followups/', SRUserFollowUpView.as_view()),
                       url(r'^api/sr/(\d+)/followup/add/', SRUserAddFollowUpView.as_view()),
                       url(r'^api/sr/(\d+)/followup/(\d+)/delete/', SRUserDeleteFollowUpView.as_view()),
                       url(r'^api/sr/(\d+)/followup/(\d+)/update/', SRUserUpdateFollowUpView.as_view()),
)
