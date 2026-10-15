from django.conf import settings


def google_map_settings(request):
    return {"ecocool_map_config": {
        "google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", "")
    }}
