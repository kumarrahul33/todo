import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from todo_manager.serializers import TaskSerializer
from todo_manager.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# view for getting the tasks

@csrf_exempt
@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all code tasks, or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # print(request.body)

        # serializer = TaskSerializer(data = json.loads(request.body.decode('utf-8')))
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def task_detail(request, pk):
    """
    Retrieve, update or delete a code task.
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        '''
        identify the task using the pk
        update the task with the new data
        '''
        print(request.data)
        task.completed = request.data['completed']
        try:
            task.name = request.data.name
        except:
            pass

        task.save()
        return HttpResponse(status=200)




    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=200)

@csrf_exempt
@api_view(['POST'])
def mark_done(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    task.completed = True
    task.save()
    return HttpResponse(status=200) 