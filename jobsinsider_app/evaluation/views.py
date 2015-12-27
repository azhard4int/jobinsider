from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.contrib.auth import login as login_session
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.core import serializers
from django.db.models import Count
from accounts import models as accounts_models
from users import models as user_models
from accounts import models as acc_mod
from core.decoraters import is_company
from accounts import forms as accountsform
from datetime import datetime
from urlparse import urlparse, parse_qs
from django.db.models import Avg, Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.template.loader import render_to_string

import models as evaluation_models

import models
import simplejson as json
import addons

@login_required()
def evaluation(request):
    return HttpResponseRedirect('/evaluation/')

# def toevaluation(request):
#     return HttpResponseRedirect('/get-evaluation-test-questions/')

class EvaluationTestTemplate(View):
    @method_decorator(login_required)
    def get(self, request):
         query = models.evaluation_test_template.objects.filter(user_id=request.user.id)

         if query:
                 return render(request, 'evaluation_index.html', {'evaluation': query})
         else:
                 return render(request, 'evaluation_index.html')

    def post(self, request):
        try:
           query=models.evaluation_test_template(
                evaluation_name=request.POST['evaluation_name'],
                evaluation_description=request.POST['evaluation_description'],
                evaluation_catagory=request.POST['evaluation_catagory'],
                evaluation_rules=request.POST['evaluation_rules'],
                evaluation_status=0,
                evaluation_type=int(request.POST['evaluation_type']),
                evaluation_time=int(request.POST['evaluation_time']),
                evaluation_total_questions=int(request.POST['evaluation_questions']),
                user_id=request.user.id
            )
           query.save()
           obj = models.evaluation_test_template.objects.latest('id')

           whole = {
               'evaluation_id':obj.id,
               'evaluation_name':request.POST['evaluation_name'],
               'evaluation_catagory':request.POST['evaluation_catagory'],
               'evaluation_status':0,
               'evaluation_type':(request.POST['evaluation_type']),
               'evaluation_time':(request.POST['evaluation_time']),
               'evaluation_total_questions':(request.POST['evaluation_questions'])
           }

           if query:
                 return HttpResponse(json.dumps({'status': whole}))
           else:
                 return HttpResponse(json.dumps({'status': 'False'}))

        except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))



class AddQuestions(View):
      def get(self, request):
        try:
            numberq = models.evaluation_test_template.objects.filter(id=request.GET['test_template_id'])
            count = models.evaluation_test_questions.objects.filter(evaluation_test_template_id=request.GET['test_template_id']).count()
            wholelist={

                'total_questions':numberq[0].evaluation_total_questions,
                'question_count':count
             }


            if (count or count==0) and numberq:
                 return HttpResponse(json.dumps({'status': wholelist}))
            else:
                 return HttpResponse(json.dumps({'status': 'False'}))
        except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))




      def post(self, request):
        try:
            numberq = models.evaluation_test_template.objects.filter(id=request.POST['id_evaluation'])
            count = models.evaluation_test_questions.objects.filter(evaluation_test_template_id=request.POST['id_evaluation']).count()

            if count < numberq[0].evaluation_total_questions:
                object = models.evaluation_test_questions(


                evaluation_question = request.POST['question'],
                evaluation_question_answer = request.POST['correct_answer'],
                evaluation_test_template_id = request.POST['id_evaluation']

                 ).save()


                obj = models.evaluation_test_questions.objects.latest('id')

                try:

                    option1 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option1'],
                    evaluation_test_template_id = request.POST['id_evaluation'],
                    evaluation_test_questions_id = obj.id

                  ).save()

                except Exception as e:
                       print e

                try:

                    option2 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option2'],
                    evaluation_test_template_id = request.POST['id_evaluation'],
                    evaluation_test_questions_id = obj.id

                ).save()

                except Exception as e:
                       print e

                try:

                    option3 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option3'],
                    evaluation_test_template_id = request.POST['id_evaluation'],
                    evaluation_test_questions_id = obj.id

                ).save()

                except Exception as e:
                       print e
                try:

                    option4 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option4'],
                    evaluation_test_template_id = request.POST['id_evaluation'],
                    evaluation_test_questions_id = obj.id

                ).save()

                except Exception as e:
                       print e

                try:

                    option5 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option5'],
                    evaluation_test_template_id = request.POST['id_evaluation'],
                    evaluation_test_questions_id = obj.id

                ).save()

                except Exception as e:
                       print e


            else:

                return HttpResponse(json.dumps({'status': 'False'}))

            return HttpResponse(json.dumps({'status': 'True'}))


        except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))



class Evaluation_Edit_Test(View):


    def get(self, request):
         try:

             query = models.evaluation_test_template.objects.filter(id=request.GET['id'], user_id=request.user.id)
             list= {
                 'id':query[0].id,
                 'evaluation_name':query[0].evaluation_name,
                 'evaluation_description':query[0].evaluation_description,
                 'evaluation_rules':query[0].evaluation_rules,
                 'evaluation_catagory':query[0].evaluation_catagory,
                 'evaluation_type':query[0].evaluation_type,
                 'evaluation_time':query[0].evaluation_time,
                 'evaluation_total_questions':query[0].evaluation_total_questions

              }
             print query
             if query:
                return HttpResponse(json.dumps({'status': list}))
             else:
                 return render(request, 'Error')

         except Exception as e:
            print e

         return HttpResponse(json.dumps({'status': 'Err'}))



    def post(self, request):
        try:
            query = models.evaluation_test_template.objects.filter(id=request.POST['evaluation_test_template_id']).update(
            evaluation_name=request.POST['edit_eva_title'],
            evaluation_description=request.POST['edit_eva_description'],
            evaluation_catagory=request.POST['edit_eva_cat'],
            evaluation_rules=request.POST['edit_eva_rules'],
            evaluation_type=int(request.POST['edit_eva_type']),
            evaluation_time=int(request.POST['edit_eva_time']),
            evaluation_total_questions=int(request.POST['edit_eva_number'])


            )
            if query:
                 return HttpResponse(json.dumps({'status': 'True'}))
            else:
                 return HttpResponse(json.dumps({'status': 'Error'}))

        except Exception as e:
                print e

        return HttpResponse(json.dumps({'status': 'Err'}))

class Evaluation_Delete_Test(View):


    def post(self, request):
         try:
            query = models.evaluation_test_template.objects.filter(id=request.POST['id'],user_id=request.user.id).delete()
            return HttpResponse(json.dumps({'status': True}))
         except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Error'}))

         return HttpResponse(json.dumps({'status': 'Err'}))




#Whole TEST

total_marks=0
class Get_Evaluation_Test_Questions(View):

    first_question = 0
    def get(self, request):
         try:
            global total_marks
            total_marks=0

            query=models.evaluation_test_questions.objects.filter(evaluation_test_template_id=request.GET['id'])
            query2 = models.evaluation_test_answer.objects.filter(evaluation_test_questions_id=query[0].id,evaluation_test_template_id=request.GET['id'])
            query3 = models.evaluation_test_template.objects.filter(id=request.GET['id'])

            global first_question
            first_question= query[0].id

            newquery=serializers.serialize('json', query2)
            length=len(query2)
            checkattempts(request.user.id,request.GET['id'])
            if query and query2:
                 return HttpResponse(json.dumps({'test_id':request.GET['id'],
                                                 'question_id':query[0].id,
                                                 'question': query[0].evaluation_question,
                                                 'length':length,
                                                 'options':newquery,
                                                  'time':query3[0].evaluation_time}))
            else:
                 return HttpResponse(json.dumps({'status': 'Error'}))

         except Exception as e:
            return HttpResponse(json.dumps({'status': 'Error'}))

    def post(self, request):

          try:
              # here calling the result function and passing the answer,question_id and evaluation test id
              cal_reult=result(request.POST['current_answer'],request.POST['test_id'],request.POST['current_question_id'])
              # to get the next question from the database
              next_question_id = get_next(request.POST['current_question_id'],request.POST['test_id'])
              # this if condidtion is to stop the test from repeat
              # if first_question != next_question_id:
              if next_question_id== 0:
                        count = models.evaluation_test_questions.objects.filter(
                            evaluation_test_template_id=request.POST['test_id']
                        ).count()
                        # print cal_reult
                        models.evaluation_result.objects.filter(user_id=request.user.id,evaluation_test_template_id=request.POST['test_id']).update(result=cal_reult)
                        number_of_attempts = models.evaluation_result.objects.filter(user_id=request.user.id,evaluation_test_template_id=request.POST['test_id'])

                        if number_of_attempts:
                            totalattempts=number_of_attempts[0].attempts
                        else:totalattempts=0

                        final_percentage = float((float(cal_reult)/float(count))*100)
                        #'questions': count
                        return HttpResponse(json.dumps({'status': 'Test is Finished', 'questions':100,'final_marks':final_percentage,'attempts':totalattempts }))
              query=models.evaluation_test_questions.objects.filter(id=next_question_id,evaluation_test_template_id=request.POST['test_id'])
              query2 = models.evaluation_test_answer.objects.filter(evaluation_test_questions_id=query[0].id,evaluation_test_template_id=request.POST['test_id'])
              newquery=serializers.serialize('json', query2)
              length=len(query2)
              if query and query2:
                       return HttpResponse(json.dumps({'test_id':request.POST['test_id'],
                                                 'question_id':query[0].id,
                                                 'question': query[0].evaluation_question,
                                                 'length':length,
                                                 'options':newquery}))
              else:
                   return HttpResponse(json.dumps({'status': 'Test is Finished'}))

          except Exception as e:
                         return HttpResponse(json.dumps({'status': 'Err'}))

# Global functions
# this is for getting the next question id
def get_next(curr_id,test_id):
    try:
        ret = models.evaluation_test_questions.objects.filter(id__gt=curr_id,evaluation_test_template_id=test_id).order_by("id")[0:1].get().id
        if not ret:
            ret=0
            return ret

    except Exception as e:
        # ret = evaluation_test_questions.objects.aggregate(Min("id"))['id__min']
        ret = 0
    return ret


# this is for callculating result
def result(user_answer,test_id,question_id):

    try:
        answer = query=models.evaluation_test_questions.objects.filter(id=int(question_id),evaluation_test_template_id=int(test_id))
        if user_answer == answer[0].evaluation_question_answer:
            global total_marks
            total_marks=total_marks+1
        return total_marks
    except Exception as e:
            return HttpResponse(json.dumps({'status': 'Err'}))


def edit_evaluation_question(request,id):
    try:
         query=models.evaluation_test_questions.objects.filter(evaluation_test_template_id=id)
         table2 = pagination_table(request.GET.get('page'),query)
         if query:
            return render(request, 'evaluation_edit_questions.html',{'query':table2})

         else:
             return render(request, 'evaluation_edit_questions.html')


    except Exception as e:
            return render(request, 'evaluation_edit_questions.html')



class Edit_Question(View):


    def get(self,request):
        try:
            questionquery=models.evaluation_test_questions.objects.filter(id=request.GET['id'])
            query=models.evaluation_test_answer.objects.filter(evaluation_test_questions_id=request.GET['id'])
            length=len(query)

            list= {

                 'question':questionquery[0].evaluation_question,
                 'answer':questionquery[0].evaluation_question_answer
            }




            newquery=serializers.serialize('json', query)

            return HttpResponse(json.dumps({'length':length,'status': newquery,'qesans':list}))

        except Exception as e:
            return HttpResponse(json.dumps({'status': 'Err'}))



    def post(self,request):

       try:


           main = models.evaluation_test_questions.objects.filter(id=request.POST['question_id'])
           question_id = request.POST['question_id']
           template_id = main[0].evaluation_test_template_id




           try:

              query = models.evaluation_test_questions.objects.filter(id=request.POST['question_id']).update(
                    evaluation_question=request.POST['question'],
                    evaluation_question_answer=request.POST['correctanswer']
                    )

           except Exception as e:
                       print e
#updating option1

           try:

                if request.POST['option2_id']:
                   option1 = models.evaluation_test_answer.objects.filter(id=request.POST['option1_id']).update(
                    evaluation_question_option=request.POST['option1']
                    )





           except Exception as e:
                       print e

#adding option1
           try:
                    try:
                        query1 = models.evaluation_test_answer.objects.filter(id=request.POST['option1_id'])
                    except Exception as e:
                        if request.POST['option1']:
                          option1 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option1'],
                    evaluation_test_template_id = template_id,
                    evaluation_test_questions_id = question_id

                  ).save()

           except Exception as e:
                       print e



#updating option 2
           try:
                  if request.POST['option2_id']:
                     option2 = models.evaluation_test_answer.objects.filter(id=request.POST['option2_id']).update(
                    evaluation_question_option=request.POST['option2']
                    )

           except Exception as e:
                       print e
#adding option 2

           try:
                    try:
                        query2 = models.evaluation_test_answer.objects.filter(id=request.POST['option2_id'])
                    except Exception as e:
                     if request.POST['option2']:
                       option2 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option2'],
                    evaluation_test_template_id = template_id,
                    evaluation_test_questions_id = question_id

                  ).save()


           except Exception as e:
                       print e


#updating option 3
           try:
                   if request.POST['option3_id']:
                       option3 = models.evaluation_test_answer.objects.filter(id=request.POST['option3_id']).update(
                    evaluation_question_option=request.POST['option3']
                    )



           except Exception as e:
                       print e
#adding option 3

           try:



                    try:
                        query3 = models.evaluation_test_answer.objects.filter(id=request.POST['option3_id'])
                    except Exception as e:
                        print "adding new entry to the data base option3"
                        if request.POST['option3']:
                           option3 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option3'],
                    evaluation_test_template_id = template_id,
                    evaluation_test_questions_id = question_id

                  ).save()
                    print "option 3 is saved"

           except Exception as e:
                       print e

#updating option 4
           try:

                if request.POST['option4_id']:
                    option4 = models.evaluation_test_answer.objects.filter(id=request.POST['option4_id']).update(
                    evaluation_question_option=request.POST['option4']
                    )

           except Exception as e:
                       print e
#adding option 4

           try:


                    try:
                        query4 = models.evaluation_test_answer.objects.filter(id=request.POST['option4_id'])
                    except Exception as e:
                        if request.POST['option4']:
                           option4 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option4'],
                    evaluation_test_template_id = template_id,
                    evaluation_test_questions_id = question_id

                  ).save()

           except Exception as e:
                       print e


#updating option 5
           try:
                 if request.POST['option5_id']:
                    option5 = models.evaluation_test_answer.objects.filter(id=request.POST['option5_id']).update(
                    evaluation_question_option=request.POST['option5']
                    )

           except Exception as e:
                       print e
#adding option 5
           try:
                    try:
                           query5 = models.evaluation_test_answer.objects.filter(id=request.POST['option5_id'])
                    except Exception as e:

                        if request.POST['option5']:
                           option5 = models.evaluation_test_answer(
                    evaluation_question_option = request.POST['option5'],
                    evaluation_test_template_id = template_id,
                    evaluation_test_questions_id = question_id

                  ).save()

           except Exception as e:
                       print e

           try:
                    if not request.POST['option1']:
                            option1 = models.evaluation_test_answer.objects.filter(id=request.POST['option1_id']).delete()
                            print 'option1 deleted'


           except Exception as e:
                               print e

           try:
                    if not request.POST['option2']:
                            option2 = models.evaluation_test_answer.objects.filter(id=request.POST['option2_id']).delete()
                            print 'option2 deleted'

           except Exception as e:
                               print e

           try:
                    if not request.POST['option3']:
                            option3 = models.evaluation_test_answer.objects.filter(id=request.POST['option3_id']).delete()
                            print "option 3 is delete"

           except Exception as e:
                               print e

           try:
                    if not request.POST['option4']:
                            option4 = models.evaluation_test_answer.objects.filter(id=request.POST['option4_id']).delete()
                            print 'option4 deleted'

           except Exception as e:
                               print e

           try:
                    if not request.POST['option5']:
                            option5 = models.evaluation_test_answer.objects.filter(id=request.POST['option4_id']).delete()
                            print 'option5 deleted'

           except Exception as e:
                               print e



           if query or option1 or option2 or option3 or option4 or option5:
            return HttpResponse(json.dumps({'status': 'True'}))
           else:
            return HttpResponse(json.dumps({'status': 'False'}))


       except Exception as e:
            return HttpResponse(json.dumps({'status': 'Err'}))


class Delete_Question(View):


    def get(self,request):
        try:
           query = models.evaluation_test_answer.objects.filter(id=request.GET['id']).delete()
           if query:
               return HttpResponse(json.dumps({'status': 'True'}))
           else:
               return HttpResponse(json.dumps({'status': 'False'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'Err'}))

    def post(self,request):
         try:
            questionquery=models.evaluation_test_questions.objects.filter(id=request.POST['id']).delete()
            if questionquery:
                return HttpResponse(json.dumps({'status': 'True'}))
         except Exception as e:
                        return HttpResponse(json.dumps({'status': 'Error'}))
         return HttpResponse(json.dumps({'status': 'True'}))



class Get_Evaluation_info(View):
    def post(self,request):
        query= evaluation_test_template.objects.filter(id=request.POST['id'])
        print query[0].evaluation_time
        list={

            'evaluation_description':query[0].evaluation_description,
            'evaluation_catagory':query[0].evaluation_catagory,
            'evaluation_rules':query[0].evaluation_rules,
            'evaluation_total_questions':query[0].evaluation_total_questions,
            'evaluation_time':query[0].evaluation_time,
            'evaluation_type':query[0].evaluation_type

        }

        return HttpResponse(json.dumps({'list':list}))


def pagination_table(page,table):
        paginator = Paginator((list(table)), 8) # Show 25 contacts per page

        try:
           table = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
           table = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            table = paginator.page(paginator.num_pages)
        return table

def checkattempts(id,test_id):
   try:
      x=models.evaluation_result.objects.filter(user_id=id,evaluation_test_template_id=test_id)
      if x:
        number=int(x[0].attempts)
        number=number+1
        models.evaluation_result.objects.filter(user_id=id,evaluation_test_template_id=test_id).update(attempts=number)
      if not x:
        models.evaluation_result(result=0,attempts=1,evaluation_test_template_id=test_id,user_id=id).save()
   except Exception as e:
         print e


def filtered_evaluation(request):
    query = models.evaluation_test_template.objects.filter(user_id=request.user.id,
                                                           evaluation_name__icontains=request.POST['search_keyword'])
    html =  render_to_string('evaluation_index_view.html', {'evaluation': query}, context_instance=RequestContext(request))
    return HttpResponse(html)