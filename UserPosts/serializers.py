from rest_framework import serializers
from .models import Posts, User

# create the posts and Retrieve the post details
class PostsSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    image = serializers.ImageField(required=False)
    video = serializers.FileField(required=False)
    class Meta:
        model = Posts
        fields = '__all__'

    def create(self, validated_data):
        user_id = self.context.get('user')
        posts= Posts.objects.create(
             user = User(id=user_id),
             title = validated_data['title'],
             description = validated_data['description'], 
             video = validated_data['video'],
             images = validated_data['images'],
        )
        return posts  
    
# perfom the post actions and Retrieve the post based on current user logged in
class PostDetilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'    