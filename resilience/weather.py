"""Opt-in official warning retrieval. It never triggers a discharge or an all-clear."""
import json
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime

URL = 'https://api.data.gov.my/weather/warning?limit=100&sort=-warning_issue__issued'

def fetch_warnings():
    if not getattr(settings,'AEROTHERMAL_LIVE_WARNINGS',False):
        return {'status':'disabled','items':[],'message':'Live warning feed is disabled. Demo scenarios are independent.'}
    cached=cache.get('aerothermal-official-warnings-v1')
    if cached is not None: return cached
    try:
        with urlopen(Request(URL,headers={'User-Agent':'AeroThermal-Hackathon/1.0','Accept':'application/json'}),timeout=5) as response:
            body=response.read(1000001)
        if len(body)>1000000: raise ValueError('Response too large')
        data=json.loads(body)
        if not isinstance(data,list): raise ValueError('Unexpected warning response')
        items=[];unparsed=0;now=timezone.now()
        for row in data:
            if not isinstance(row,dict): continue
            start=parse_datetime(str(row.get('valid_from','')))
            end=parse_datetime(str(row.get('valid_to','')))
            if start is None or end is None:
                unparsed+=1;continue
            if timezone.is_naive(start): start=timezone.make_aware(start,ZoneInfo('Asia/Kuala_Lumpur'))
            if timezone.is_naive(end): end=timezone.make_aware(end,ZoneInfo('Asia/Kuala_Lumpur'))
            if start <= now < end:
                issue=row.get('warning_issue') or {}
                items.append({'title':row.get('heading_en') or issue.get('title_en') or row.get('heading_bm','Warning'),
                              'text':row.get('text_en') or row.get('text_bm',''),
                              'instruction':row.get('instruction_en') or row.get('instruction_bm',''),
                              'valid_to':end.isoformat()})
        result={'status':'retrieved','items':items,'retrieved_at':now.isoformat(),
                'message':f'Latest 100 national records checked; {unparsed} unparseable records omitted. Location relevance requires operator review. Empty results are not an all-clear.'}
    except Exception:
        result={'status':'unavailable','items':[],'message':'Official warning feed unavailable. No all-clear or local forecast is inferred.'}
    cache.set('aerothermal-official-warnings-v1',result,300 if result['status']=='retrieved' else 60)
    return result
