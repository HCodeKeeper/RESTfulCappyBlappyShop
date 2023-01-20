from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse


def process_ajax(request, json, method='GET') -> JsonResponse:
    if not is_ajax(request):
        return HttpResponseBadRequest('Invalid request')
    else:
        if request.method == method:
            return JsonResponse(json)
        return JsonResponse({'status': 'Invalid request'}, status=400)


def is_ajax(request: HttpRequest):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    return False
