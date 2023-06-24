from .serializers import PostsSerializers, PostDetilesSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Posts, User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

# creating the new posts and Retrieve the post details
class UserPosts(APIView):
   # creating a posts
    def post(self, request, format=None):
        # request.user.id = 1
        serializers = PostsSerializers(data=request.data, context={'user':request.user.id})
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'post created successfull'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Retrieve all the post details
    def get(self, request, format=None):
        queryset = Posts.objects.all()
        serializers = PostsSerializers(queryset, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK)

#update and delete the post
class PostActions(RetrieveUpdateDestroyAPIView):
     queryset = Posts.objects.all()
     serializer_class = PostDetilesSerializers
    #  delete the posts
     def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Post delete successful'}, status=status.HTTP_204_NO_CONTENT)
     
     # update the posts
     def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Post update successful'}, status=status.HTTP_200_OK) 


# this view should return a list of all the post for the currently login user.
class PostDetailsCurrentUser(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PostDetilesSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        print(user_id)
        return Posts.objects.filter(user=user_id)



         
