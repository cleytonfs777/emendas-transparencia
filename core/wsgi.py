import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

from core.settings import BASE_DIR  # Import BASE_DIR from settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(
    BASE_DIR, 'fotosbm', 'imagem_disparo'), prefix='/media/')
