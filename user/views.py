from django.conf import settings
from django.contrib.auth import user_logged_in
from django.utils import timezone
from jose import jwt, ExpiredSignatureError, JWTError
from knox.models import AuthToken
from knox.views import LoginView, LogoutView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Return the User object corresponding on the currently authenticated user.
        """
        current_user = request.user
        serializer = UserSerializer(current_user)
        return Response(serializer.data)


class UserLoginView(LoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Allow user to log in using a signed JWT.
        JWT is specified in request body or X-AUTH-JWT header.
        """
        # Prefer getting JWT by request body (json or form, supplied by DRF)
        auth_jwt = request.data.get('jwt', None)

        # Alternatively, get JWT from request X-AUTH-JWT header
        if not auth_jwt:
            auth_jwt = request.META.get('HTTP_X_AUTH_JWT', None)

        # If JWT not found, return error
        if not auth_jwt:
            raise AuthenticationFailed(detail="JWT missing or of an incorrect format.")

        try:
            payload = jwt.decode(auth_jwt, settings.AUTH_JWT_PUBLIC_KEY,
                                 algorithms=settings.AUTH_JWT_VALID_ALGORITHMS,
                                 options=settings.AUTH_JWT_OPTIONS,
                                 audience='https://api.timecheck.app',
                                 issuer='https://id.mattcorp.com',
                                 subject='MattCorpAccountCredential')
        except ExpiredSignatureError:
            raise AuthenticationFailed(detail="JWT expired.")
        except JWTError:
            raise AuthenticationFailed(detail="JWT invalid.")

        if not {'iss', 'iat', 'exp', 'aud', 'sub'}.issubset(payload.keys()):
            raise AuthenticationFailed(detail="JWT invalid.")

        mattcorp_id = payload.get('uid', None)
        claims = payload.get('claims', None)

        if not mattcorp_id or not claims:
            raise AuthenticationFailed(detail="JWT invalid.")

        name = claims.get('fullName', None)
        email = claims.get('emailAddress', None)
        email_verified = claims.get('emailVerified', None)

        if name is None or email is None or email_verified is None:
            raise AuthenticationFailed(detail="JWT invalid.")

        try:
            user = User.objects.get(mattcorp_id=mattcorp_id)
            # TODO: Create background job to update user properties
        except User.DoesNotExist:
            user = User.objects.create_user(mattcorp_id=mattcorp_id,
                                            name=name,
                                            email=email,
                                            email_verified=email_verified)
            # TODO: Any 'welcome to TimeCheck' tasks (i.e. welcome email)
        # (slightly modified) Knox code
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = user.auth_token_set.filter(expires__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {'error': "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        token = AuthToken.objects.create(user, token_ttl)[1]
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)
        if UserSerializer is None:
            return Response({
                'token': token
            })
        return Response({
            'details': UserSerializer(user).data,
            'token': token,
        })


class UserLogoutView(LogoutView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def get(self, request):
        # TODO: Implement some way to log out of all sessions (as a user option)
        return super().post(request)
