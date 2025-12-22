import typing as tp
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import  Admin, Users , History
from tortoise import Tortoise

from fastadmin import TortoiseModelAdmin, WidgetType, action, display
from fastadmin import fastapi_app as admin_app
from fastadmin import register
import json


@register(Admin)
class UserModelAdmin(TortoiseModelAdmin):
    list_display = ("id", "username", "is_superuser")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser")
    search_fields = ("username",)
    formfield_overrides = {  # noqa: RUF012
        "username": (WidgetType.SlugInput, {"required": True}),
        "password": (WidgetType.PasswordInput, {"passwordModalForm": True}),
        "avatar_url": (
            WidgetType.Upload,
            {
                "required": False,
                # Disable crop image for upload field
                # "disableCropImage": True,
            },
        ),
    }

    async def authenticate(self, username: str, password: str) -> uuid.UUID | int | None:
        obj = await self.model_cls.filter(username=username, password=password, is_superuser=True).first()
        if not obj:
            return None
        return obj.id

    async def change_password(self, id: uuid.UUID | int, password: str) -> None:
        user = await self.model_cls.filter(id=id).first()
        if not user:
            return
        # direct saving password is only for tests - use hash
        user.password = password
        await user.save()

    async def orm_save_upload_field(self, obj: tp.Any, field: str, base64: str) -> None:
        # convert base64 to bytes, upload to s3/filestorage, get url and save or save base64 as is to db (don't recomment it)
        setattr(obj, field, base64)
        await obj.save(update_fields=(field,))



@register(Users)
class UsertModelAdmin(TortoiseModelAdmin):
     list_display = ("id", "username", "prompts_remaining", "first_time_connection", "last_time_use")
from fastadmin import display
@register(History)
class HistoryModelAdmin(TortoiseModelAdmin):
    list_display = ("id", "get_user_info", "history_summary", "created_at")
    
    async def get_queryset(self, request):
        """Charger les données avec prefetch_related"""
        qs = await super().get_queryset(request)
        return qs.prefetch_related("user")
    @display
    def get_user_info(self, obj):
        """Accéder au user depuis le QuerySet"""
        try:
            # obj.user est un QuerySet, pas un objet User
            # Vous devez récupérer le premier élément
            
            # Méthode 1: Vérifier si c'est un QuerySet
            if hasattr(obj.user, 'all'):  # C'est un QuerySet
                # Essayer d'obtenir le premier user
                user_query = obj.user
                
                # Vérifier si le QuerySet a des résultats en cache
                if hasattr(user_query, '_result_cache') and user_query._result_cache:
                    # Prendre le premier résultat
                    user = user_query._result_cache[0]
                    if user and hasattr(user, 'username'):
                        return f"{user.username} (ID: {user.id})"
                
                # Sinon, utiliser user_id
                return f"User ID: {obj.user_id}"
            
            # Méthode 2: Si par miracle c'est déjà un objet User
            elif hasattr(obj.user, 'username'):
                return f"{obj.user.username} ({obj.user.id})"
            
            # Fallback
            return f"User ID: {obj.user_id}"
            
        except Exception as e:
            return f"Error: {str(e)[:30]}"
    
    get_user_info.short_description = "Utilisateur"
    @display
    def history_summary(self, obj):
        """Résumé de l'historique"""
        if obj.history and isinstance(obj.history, list):
            return f"{len(obj.history)}"
        return "0 entrée"
    
 




async def init_db():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["models"]})
    await Tortoise.generate_schemas()


async def create_superuser():
    print("c est nous les super")
    await Admin.create(
        username="admin",
        password="admin",
        is_superuser=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    #await create_superuser()
    yield
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


app.mount("/admin", admin_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)