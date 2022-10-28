from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from notes.notes.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from notes.notes.models import Label
from notes.notes.serializers import LabelSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def label_list(request):
    """
    List all code group notes, or create a new group note.
    """
    if request.method == 'GET':
        group_notes = Label.objects.all()
        serializer = LabelSerializer(group_notes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def label_detail(request, pk):
    """
    Retrieve, update or delete a code group note.
    """
    try:
        group_note = Label.objects.get(pk=pk)
    except Label.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LabelSerializer(group_note)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LabelSerializer(group_note, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        group_note.delete()
        return HttpResponse(status=204)
