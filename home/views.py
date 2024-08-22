from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.decorators import async_only_middleware
from .models import Question, Choice
from .forms import QuestionForm
from django.contrib.auth.models import User
import IP2Location

# Initialize IP2Location database
db = IP2Location.IP2Location("db/IP2LOCATION-LITE-DB1.BIN")

# Synchronous function to get country
def get_country(request):
    user_ip = request.META.get('REMOTE_ADDR')  # Get the user's IP address
    record = db.get_all(user_ip)
    country = record.country_short
    return country

class IndexView(generic.ListView):
    template_name = "home/index.html"
    context_object_name = "question_list"
    users = User.objects.filter(is_superuser=False)

    async def get_queryset(self):
        # Handle synchronous database operations correctly
        queryset = await database_sync_to_async(Question.objects.filter)(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")
        return queryset

    async def get(self, request, *args, **kwargs):
        # Call the synchronous function in an async view
        country = get_country(request)
        context = {
            'users': self.users,
            'country': country,
        }
        return await super().get(request, *args, **kwargs)

class DetailView(generic.DetailView):
    model = Question
    template_name = "home/detail.html"

    async def get_queryset(self):
        queryset = await database_sync_to_async(Question.objects.filter)(
            pub_date__lte=timezone.now()
        )
        return queryset

class ResultsView(generic.DetailView):
    model = Question
    template_name = "home/results.html"

async def vote(request, question_id):
    question = await database_sync_to_async(get_object_or_404)(Question, pk=question_id)
    try:
        selected_choice = await database_sync_to_async(question.choice_set.get)(pk=request.POST["choice"])
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
        await database_sync_to_async(selected_choice.save)()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("home:results", args=(question.id,)))

@login_required
@async_only_middleware
async def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            await database_sync_to_async(form.save)()
            return redirect("/home")
    else:
        form = QuestionForm()
    return render(request, 'addquestion.html', {'form': form})

