import re
from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth.models import User

from account.models import User, Permission, Project, Role, UserData

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if password:
            regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
            pattern = re.compile(regular_expression)
            valid1 = re.search(pattern, password)
            if not valid1:
                raise serializers.ValidationError(
                    "Password must be at least 8 characters long, uppercase and lowercase letters,one numeric character and special character"
                )

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data  

class PermissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Permission
        fields = ('id', 'project','user', 'role', 'read', 'delete', 'update')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_name', 'project_slug')

class UserDataSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer()
    project = ProjectSerializer()

    class Meta:
        model = UserData
        fields = ('id','user', 'project', 'permission', 'role', 'status')
