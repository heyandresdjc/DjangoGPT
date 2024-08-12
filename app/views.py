from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from app.forms import QuestionForm, TrainingFileForm
from app.models import Answer, Question, TrainingFile
from llm_interface import run_llm


def handle_queries(form):
    question_str = form.cleaned_data["question"]
    result = run_llm(
        question=question_str,
    )

    question_obj = Question(
        question=question_str,
    )

    question_obj.save()
    Answer(
        question=question_obj,
        answer=result["result"],
    ).save()


def homepage(request):
    form = QuestionForm()
    answers = Answer.objects.all()[:3]
    questions = Question.objects.all()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            handle_queries(form)
            return redirect("index")

    return render(
        request,
        'app/index.html',
        {
            "form": form,
            "answers": answers,
            "questions": questions,
        }
    )


class AddTrainingDataView(CreateView):
    model = TrainingFile
    form_class = TrainingFileForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["files"] = TrainingFile.objects.all()
        return context
