from celery import shared_task
from app.models import TrainingFile
from llm_interface import add_document


@shared_task
def add_to_vector(training_file_id):
    training_file = TrainingFile.objects.get(id=training_file_id)
    print("*"*80)
    print(training_file.file.path)
    results = add_document()
    if results:
        training_file.is_ran = True
        training_file.save()

    return True, "Finish adding"
