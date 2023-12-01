from django.db import models

# Create your models here.

USER_TYPE_CHOICES = (
    ('OP', 'Operations User'),
    ('CL', 'Client User'),
)

FILES_TYPES=(('pptx', 'PowerPoint'), ('docx', 'Word Document'), ('xlsx', 'Excel Spreadsheet'))

class User(models.Model):
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    passwrd=models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.username}'

class File(models.Model):
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILES_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self) -> str:
        return f'{self.file_name}'