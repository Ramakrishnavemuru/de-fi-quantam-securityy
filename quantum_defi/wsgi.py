"""
WSGI config for quantum_defi project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum_defi.settings')

application = get_wsgi_application()

