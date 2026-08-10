from django.db import connections
from django.http import JsonResponse


def api_root(request):
    return JsonResponse(
        {
            "status": "ok",
            "health": "/api/health/",
            "schema": "/api/schema/",
            "documentation": "/api/swagger/",
        }
    )


def health(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "unhealthy"}, status=503)

    return JsonResponse({"status": "ok"})
