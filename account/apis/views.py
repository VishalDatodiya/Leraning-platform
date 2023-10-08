from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from account.models import User, Role, Project, Permission, UserData

from account.apis.serializers import LoginSerializer, PermissionSerializer, ProjectSerializer, UserDataSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'message':"Login Successfully",
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
class Login(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_tokens_for_user(user)
        return Response({"token":token}, status=status.HTTP_200_OK)
        
        
    
# class UserListingView(APIView):
    
#     def get(self, request):
#         user_info = Permission.objects.all()
#         serializer = UserDataSerializer(user_info, many=True)
#         # serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        

# class UserListingView(APIView):
    
#     def get(self, request):
#         user_info = Permission.objects.all()
#         data = []
#         for permission in user_info:
#             user_data = {
#                 'username': permission.user.username,
#                 'emp-id': permission.user.emp_id,
#                 'project_name': permission.project.project_name,
#                 'read_permission': permission.read,
#                 'delete_permission': permission.delete,
#                 'update_permission': permission.update
#             }
#             data.append(user_data)
#         return Response(data, status=status.HTTP_200_OK)

class UserListingView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    
    # queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    

    def get_queryset(self):
            pk = self.kwargs['pk']  
            return Permission.objects.filter(project=pk)


# views.py

# class UserDetail(generics.ListAPIView):
#     serializer_class = ProjectSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['pk']
#         print(user_id)  
#         return UserData.objects.filter(user_id=user_id).select_related('project')



# class UserDetail(APIView):
    
#     def get(self, request, emp_id):
#         print(emp_id)
#         try:
#             # Retrieve user data based on emp_id
#             user_data = UserData.objects.filter(user__emp_id=emp_id)
#             print(user_data)
#             serializer = UserDataSerializer(user_data, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except UserData.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        
        
        
        
