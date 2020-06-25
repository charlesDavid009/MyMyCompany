from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from blog.serializers import(ItemSerializer,
                              ViewerSerializer,
                              ActionBlogSerializer,
                              SubViewerSerializer
                              )
from blog.models import Items, Viewers, PostLikes, SubViewers
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated




# Create your views here.


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def items_list(request):
    """
    list of items or create a new line
    """
    if request.method == 'GET':
        item = Items.objects.order_by('-created_at')
        serializer =ItemSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_blog(request, *args, **kwargs):
    """
    CREATE BLOG API
    """
    if request.method == 'POST':
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def action(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        serializer = ActionBlogSerializer(data= request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            details = data.get("details")
            qs = Items.objects.filter(id =blog_id)
            if not qs.exsits():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(request.user)
                serializer = ItemSerializer(obj)
                return Response(serializer.data)
            elif action =="Unlike":
                obj.like.add(request.user)
            elif action =="Re_post":
                new_blog = Items.objects.create(
                    user= request.user,
                    parent = obj,
                    details = details
                )
                serializer = ItemSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def comment(request, id, *args, **kwargs):
    """
    ADD COMMENT TO POST /BLOG
    """
    try:
        item = Items.objects.get(id=id)
    except Items.DOESNOTEXIST:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = ViewerSerializer( item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def sub_comment(request, id, *args, **kwargs):
    """
    ADD A SUB COMMENT TO A COMMENT
    """
    try:
        item = Viewers.objects.get(id=id)
    except Items.DOESNOTEXIST:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = SubViewerSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def comment_details(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        qs =Viewers.objects.filter(reference = id).order_by('-created_at')
        serializer = ViewerSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def items_details(request, pk,  *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    AND YOU CAN GET A PARTICULAR POST OR DELETE
    """
    try:
        item = Items.objects.get(pk=pk)
    except Items.DOESNOTEXIST:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = ItemSerializer(item)
        qs = Viewers.objects.filter(reference=pk).order_by('-created_at')
        if qs.exists():
            serializer = ViewerSerializer(qs, many=True)
            data ={
               "blog": serializers.data,
                "comments": serializer.data
            }
            return Response(data)
        return Response(serializers.data)


@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def items_delete(request, pk,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    try:
        item = Items.objects.get(pk=pk).filter(user=request.user)
    except Items.DOESNOTEXIST:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        item.delete()


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, pk,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE COMMENT
    """
    try:
        item = Viewers.objects.get(pk=pk)
    except Items.DOESNOTEXIST:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        src = item.filter(user=request.user)
        if not src.exists():
            return Response({}, status=status.HTTP_401_NOT_AUTHORISED)
        qs = SubViewers.objects.filter(reference=pk)
        if qs.exists():
            dates = {
                "blog": qs,
                "comments": scr
            }
            dates.delete()
        src.delete()







