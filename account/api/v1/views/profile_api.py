from rest_framework import generics
from django.shortcuts import get_object_or_404
from ....models.profile import Profile
from ..serializers.profile_serializers import  ProfileSerializer
from rest_framework.permissions import IsAuthenticated



# class ProfileEditApi(generics.UpdateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return get_object_or_404(
#             Profile,
#             user=self.request.user
#         )
   



class MyProfileViewApi(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    def get_object(self):
        return get_object_or_404(
            Profile,
            user=self.request.user
        )