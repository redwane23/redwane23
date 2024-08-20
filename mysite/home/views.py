from django.shortcuts import get_object_or_404, render,redirect
from .models import Question,Choice
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .forms import QuestionForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import IP2Location
from django.http import JsonResponse

db = IP2Location.IP2Location("db/IP2LOCATION-LITE-DB1.BIN")

def get_country(request):
    user_ip = request.META.get('REMOTE_ADDR')  # Get the user's IP address
    record = db.get_all(user_ip)
    country = record.country_short

    return country

class IndexView(generic.ListView):
    template_name = "home/index.html"
    context_object_name = "question_list"
    users=User.objects.filter(is_superuser=False)
    country=get_country
    extra_context = {'users': users,'country':country}
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by
        ("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "home/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "home/results.html"

    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "home/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("home:results", args=(question.id,)))
@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.user = request.user 
            form.save()
            return redirect("/home")
    else:
        form=QuestionForm()
    return render(request,'addquestion.html',{'form':form})
