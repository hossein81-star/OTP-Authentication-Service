from rest_framework.views import APIView
from ..serializers.logout import UserLogoutSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from drf_spectacular.utils import extend_schema,OpenApiResponse


class UserLogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UserLogoutSerializer,
        responses={
            200: OpenApiResponse(description="Logout successful"),
            400: OpenApiResponse(description="Invalid refresh token"),
        },
        tags=["Auth"],
    )
    def post(self, request):
        serializer = UserLogoutSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Logout successful."},
            status=status.HTTP_200_OK,
        )