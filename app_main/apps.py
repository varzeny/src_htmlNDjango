from django.apps import AppConfig

import utils.utils_network as nt



class AppMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_main'
    



NETWORKCONTROLLER = nt.NetworkController()