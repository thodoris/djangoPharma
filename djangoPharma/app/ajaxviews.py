import drugs.cacheService as cacheService
import drugs.migrationService as migrationService
from django.http import JsonResponse

def syncdb(request):
    """Renders the home page."""
    result=migrationService.synchronize_data()
    data = {
        'result': result
    }
    if data['result'] is None:
        data['error_message'] = 'An error occured while synchronizing local DB'
    return JsonResponse(data)
