from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from notes.notes.serializers.note_serializer import NoteSerializer
from notes.notes.serializers.user_serializer import UserSerializer
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from notes.notes.models import Label, Note
from notes.notes.serializers import LabelSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class NoteList(APIView):
    """
    List all notes, or create a new note
    """

    def get(self, request, format=None):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetail(APIView):
    """
    Retrieve, update or delete a note instance.
    """

    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LabelListCreate(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def label_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code group note.
    """
    try:
        group_note = Label.objects.get(pk=pk)
    except Label.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LabelSerializer(group_note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LabelSerializer(group_note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group_note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
