from rest_framework import serializers
from account.models import User

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .util import sent

class UserRegistrationSerializers(serializers.ModelSerializer):
    # we are writting this becoz we need confirm password field 
    password2 = serializers.CharField(style={'input_type':'password','write_only':True})
    class Meta:
        model= User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    # Validating password and confirm password while registration    
    def validate(self, validated_data):
            password = validated_data.get('password')
            password2= validated_data.get('password2')
            if (password != password2):
                raise serializers.ValidationError("password and confirm passowrd doesn't match")
            return validated_data
        
    def create(self, validated_data):
            return User.objects.create_user(**validated_data)
    

# log in
class UserLoginSerializers(serializers.ModelSerializer):
      email = serializers.CharField(max_length=255)
      class Meta:
            model = User
            fields = ['email', 'password']   

# Retrieve the user profile for login use
class userProfileSerializers(serializers.ModelSerializer):
      class Meta:
            model = User
            fields = ['id','email', 'name']           

# change the password
class UserChangePass_Serializers(serializers.ModelSerializer):
       password = serializers.CharField(max_length=255,style={'input_type':'password','write_only':True} )
       password2 = serializers.CharField(max_length=255,style={'input_type':'password','write_only':True} )
       
       class Meta:
            model = User
            fields = ['password', 'password2']

       def validate(self, validated_data):
            password = validated_data.get('password')
            password2 = validated_data.get('password2')
            user = self.context.get('user')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            user.set_password(validated_data['password'])
            user.save()
            return validated_data      
       

# sent mail for change password link
class SentPasswordResetEmailSerializers(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255) 
    class Meta:
        model = User
        fields = ['email']

    def validate(self, validated_data):
            email = validated_data.get('email')
        
            if User.objects.filter(email = email).exists():
                user=User.objects.get(email = email) 
                uid = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
                # Send EMail
                body = 'Click Following Link to Reset Your Password '+link 
                email = user.email
                sent(email,body)
                return validated_data
            else:
               raise serializers.ValidationError('You are not a Registered User')


# password rest vaildation
class PasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password', 'password2']  

    def validate(self, validated_data):
        try:
            password = validated_data.get('password')
            password2 = validated_data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(validated_data['password'])
            user.save()
            return validated_data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired') 