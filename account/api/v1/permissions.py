from rest_framework.permissions import BasePermission

class IsUserProfile(BasePermission):
     def has_object_permission(self, request, view, obj):
          user_id=request.user
          if obj.user == user_id:
               return True
          return False