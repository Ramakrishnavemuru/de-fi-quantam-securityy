"""
ASGI config for quantum_defi project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum_defi.settings')

application = get_asgi_application()

