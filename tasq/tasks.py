from celery import shared_task


@shared_task
def big_data(arr):
    return arr
