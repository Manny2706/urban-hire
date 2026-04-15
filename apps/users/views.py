from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLogoutSerializer, UserSignupSerializer ,UserLoginSerializer



class UserSignupView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = UserSignupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		refresh = RefreshToken.for_user(user)

		return Response(
			{
				'message': 'Customer registered successfully.',
				'customer': {
					'id': user.id,
					'username': user.username,
					'email': user.email,
					'first_name': user.first_name,
					'last_name': user.last_name,
				},
				'tokens': {
					'access': str(refresh.access_token),
					'refresh': str(refresh),
				},
			},
			status=status.HTTP_201_CREATED,
		)


class UserLogoutView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = UserLogoutSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(
			{'message': 'Customer logged out successfully.'},
			status=status.HTTP_200_OK,
		)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'Customer logged in successfully.',
                'customer': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )