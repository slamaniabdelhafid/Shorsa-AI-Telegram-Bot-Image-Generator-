from enum import Enum

from tortoise import fields
from tortoise.models import Model
from typing import List, Any


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Admin(BaseModel):
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)

    avatar_url = fields.TextField(null=True)
    

    def __str__(self):
        return self.username

    class Meta:
        table = "admin"



class Users(BaseModel):
    username = fields.CharField(max_length=50, unique=True)
    id = fields.IntField(pk=True)
    is_active = fields.BooleanField(default=True)  
    prompts_remaining = fields.IntField(default=0)

    first_time_connection = fields.DatetimeField(auto_now=True)
    last_time_use = fields.DatetimeField(auto_now=True)

    def str(self):
        return self.username
    
    class Meta:
        table = "users"

class History(BaseModel):
    # Relation ForeignKey vers Users
    user = fields.ForeignKeyField(
        'models.Users', 
        #related_name='histories', 
        on_delete=fields.CASCADE
    )
    id = fields.IntField(pk=True)
    history = fields.JSONField(default=list)  
    created_at = fields.DatetimeField(auto_now_add=True)

    def str(self):
        return f"History for {self.user.username}"
    
    class Meta:
        table = "history"
