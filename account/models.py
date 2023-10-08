from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class AbstractTable(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Role(AbstractTable):
    SUPERADMIN = 1
    PROJECT_MANAGER = 2
    ASSISTANT_PROJECT_MANAGER = 3
    TEAM_LEAD = 4
    AGENT = 5

    ROLE_CHOICES = (
        (SUPERADMIN, "Super Admin"),
        (PROJECT_MANAGER, "Project Manager"),
        (ASSISTANT_PROJECT_MANAGER, "Assistant Project Manager"),
        (TEAM_LEAD, "Team Lead"),
        (AGENT, "Agent"),
    )
    role = models.IntegerField(choices=ROLE_CHOICES)

    class Meta:
        db_table = "roles"

    def get_role_display_str(self):
        return dict(self.ROLE_CHOICES).get(self.role)

    def __str__(self):
        return f"{self.get_role_display_str()}"
    
    
class Project(AbstractTable):
    project_name = models.CharField(max_length=200)
    project_slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.project_name

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    # emp_id = models.CharField(primary_key=True, max_length=100)
    projects = models.ManyToManyField('Project', through='UserData', related_name='users')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class Permission(AbstractTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    

class UserData(AbstractTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="user_data")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    STATUS_CHOICES = ((1, "Active"), (0, "Inactive"))
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return str(self.user)
