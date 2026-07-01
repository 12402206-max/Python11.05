from .cinema_controller import cinema_bp
from .dashboard_controller import dashboard_bp
from .api.cinema_api import api_cinema_bp

__all__ = ["cinema_bp", "dashboard_bp", "api_cinema_bp"]
