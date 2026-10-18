import re
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import StakeholderAccess

class ResidentBoundaryMiddleware:
    """Residents use the resident portal; existing corporate endpoints remain private."""
    def __init__(self,get_response): self.get_response=get_response
    

    def __call__(self,request):
        match=re.match(r'^/(?:api/)?projects/(\d+)(?:/|$)',request.path)
        if match and request.user.is_authenticated:
            pid=int(match[1])
            resident=StakeholderAccess.objects.filter(membership__project_id=pid,membership__user=request.user,resident_only=True).exists()
            if resident:
                return HttpResponseForbidden('This website is a B2B workspace. Resident access belongs to the mobile app.')
        return self.get_response(request)
