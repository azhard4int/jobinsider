from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class evaluation_test_template(models.Model):
    evaluation_name = models.CharField(blank=True,max_length=255,default=None)
    evaluation_description = models.CharField(blank=True, max_length=255)
    evaluation_catagory = models.CharField(blank=True, max_length=255)
    evaluation_rules = models.CharField(blank=True, max_length=255)
    evaluation_status = models.IntegerField(default=0,blank=True)#Test status 0 appending and 1 approved
    evaluation_time = models.IntegerField(default=20,blank=True)
    evaluation_type = models.BooleanField(default=0,blank=True)# 0 for True/False and 1 is for MCQ
    evaluation_total_questions = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.evaluation_name)


class evaluation_test_questions(models.Model):
    evaluation_question = models.CharField( blank=True,max_length=255,default=None)
    evaluation_question_answer = models.CharField( blank=True,max_length=255)
    evaluation_test_template = models.ForeignKey(evaluation_test_template)
    def __unicode__(self):
        return unicode(self.evaluation_question)


class evaluation_test_answer(models.Model):
    evaluation_question_option = models.CharField( blank=True,max_length=255,default=None)
    evaluation_test_template = models.ForeignKey(evaluation_test_template)
    evaluation_test_questions = models.ForeignKey(evaluation_test_questions)

    def __unicode__(self):
        return unicode(self.evaluation_question_option)


class evaluation_result(models.Model):
    result = models.CharField( blank=True,max_length=255,default=None)
    evaluation_test_template = models.ForeignKey(evaluation_test_template)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.result)