from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from core.api.serializers.label import LabelSerializer
from core.models import Label


class LabelListCreate(ListCreateAPIView):
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
        return Http404

    if request.method == 'GET':
        serializer = LabelSerializer(group_note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LabelSerializer(group_note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group_note.delete()
        return Response(status=HTTP_204_NO_CONTENT)
