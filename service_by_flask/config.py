try:
    from .local_settings import *
except ImportError:
    from .produce_settings import *
