from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

# Create your models here.
class Tasks(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts", null=True , default= "blog/images/coding.jpg")
    due_date = models.DateField()
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    is_completed = models.BooleanField(default=False)  
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(max_length=20, default='Low', choices=PRIORITY_CHOICES)
    
    def save(self, *args, **kwargs):
        # Generate the slug based on the title
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tasks, self).save(*args, **kwargs)