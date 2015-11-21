__author__ = 'V'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *


from . import views

urlpatterns = patterns(
    url(r'', evaluation),
    url(r'^$', EvaluationTestTemplate.as_view(), name='test_template'),
    url(r'^index/$', EvaluationTestTemplate.as_view(), name='test_template'),
    url(r'^testing/sample/(?P<id>[0-9]+)$', edit_evaluation_question, name='edit_evaluation_test'),
    url(r'^edit/question-options/$', Edit_Question.as_view(), name='Edit_Question'),
    url(r'^edit/question-options/delete/$', Delete_Question.as_view(),name='Delete_Question'),
    url(r'^addquestions/$', AddQuestions.as_view(), name='Add-questions'),
    url(r'^add-evaluation-test-template/$', EvaluationTestTemplate.as_view(), name='test_template'),
    url(r'^edit-evaluation-test-template/$', Evaluation_Edit_Test.as_view(), name='edit-evaluation-test'),
    url(r'^delete-evaluation-test-template/$', Evaluation_Delete_Test.as_view(), name='delete-evaluation-test'),
    url(r'^get-evaluation-test-questions/$', Get_Evaluation_Test_Questions.as_view(), name='delete-evaluation-test')
)