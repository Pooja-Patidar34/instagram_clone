
import os
import django
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import core.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_clone.settings')
django.setup()

application = ProtocolTypeRouter({
          "http":get_asgi_application(),
          "websocket":AuthMiddlewareStack(
                    URLRouter(
                              core.routing.websocket_urlpatterns
                    )
          ),
})
