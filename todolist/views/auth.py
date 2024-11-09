from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import views, permissions, status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from todolist.serializers.auth import RegisterUserSerializer


# {"username":"lisa","password":"hrenWam@mail.ru"}

class RegisterUserGenericView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)  #
        serializer.is_valid(raise_exception=True)  #
        serializer.save()  #
        headers = self.get_success_headers(serializer.data)  #
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh_token = RefreshToken.for_user(user)
            # access_token = str(refresh_token.assets_token)
            access_token = refresh_token.access_token

            access_expiry = datetime.utcfromtimestamp(access_token['exp'])
            refresh_expiry = datetime.utcfromtimestamp(refresh_token['exp'])

            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=str(access_token), httponly=True, secure=False, samesite='Lax', expires=access_expiry, )
            response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True, secure=False, samesite='Lax', expires=refresh_expiry, )
            return response
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class RefreshTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            access_expiry = datetime.utcfromtimestamp(access_token['exp'])
            refresh_expiry = datetime.utcfromtimestamp(refresh_token['exp'])

            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=str(access_token), httponly=True, secure=False, samesite='Lax', expires=access_expiry, )
            response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True, secure=False, samesite='Lax', expires=refresh_expiry, )
            return response
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)










