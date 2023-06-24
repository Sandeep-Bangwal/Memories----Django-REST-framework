from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.Serializers import UserRegistrationSerializers ,UserLoginSerializers, userProfileSerializers,SentPasswordResetEmailSerializers, UserChangePass_Serializers, PasswordResetSerializer
from django.contrib.auth import authenticate, login
from account.render import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# creating the tokens 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# user Registration
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        serializers = UserRegistrationSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
            token = get_tokens_for_user(user)
            return Response({'token':token ,'msg': 'Registration Successful..'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
# user login view    
class UserLoginView(APIView):
     renderer_classes = [UserRenderer]
     def post(self, request, format = None):
        serializers = UserLoginSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            email = serializers.data.get('email')
            password = serializers.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                login(request, user)
                # calling the token genrating view
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg': 'Login Successful..'}, status=status.HTTP_200_OK)
            else:
               return Response({'errors': {'non_field_errors':['email or password not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# get the user profile
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
       serializers = userProfileSerializers(request.user)  
       return Response(serializers.data, status=status.HTTP_200_OK)

# change the old password
class UserChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
       serializers = UserChangePass_Serializers(data=request.data, context={'user':request.user}) 
       if serializers.is_valid(raise_exception=True):
        return Response({'msg': 'Password Change Successfully'}, status=status.HTTP_200_OK)
       else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# sent the rest password links
class SentPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
       serializers = SentPasswordResetEmailSerializers(data=request.data) 
       if serializers.is_valid():
        return Response({'msg': 'Password Reset Link send Please chek yopur Email'}, status=status.HTTP_200_OK)
       return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# vaildate and update the reset password
class PasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
     serializer = PasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
     serializer.is_valid(raise_exception=True)
     return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

