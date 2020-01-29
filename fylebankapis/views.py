import json
from django.core import serializers
from django.db.models import CharField
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Branches


class HomePage(View):
    def get(self, request):
        try:
            home_page_content = """<h1>Hello there!</h1> </br>Please use 
            http://fyle-apis.herokuapp.com/api/branches/autocomplete?q=RTGS&limit=3&offset=0</br>
            and </br>
            http://fyle-apis.herokuapp.com/api/branches?q=Bangalore&limit=2&offset=1
            to test the APIs"""
            return HttpResponse(home_page_content, status=200)
        except Exception as e:
            return Response(status=500)


class AutoComplete(APIView):

    def get(self, request):
        try:
            branch_name = request.query_params.get('q', None)
            if not branch_name:
                raise ValueError()
            limit = request.query_params.get('limit', 3)
            offset = request.query_params.get('offset', 0)
            bb = Branches.objects.filter(branch__istartswith=branch_name).order_by('-ifsc')[int(offset):int(limit)]
            branch_data = serializers.serialize("json", bb)
            branch_data = json.loads(branch_data)
            autocomplete_data = {}
            data = []
            for branch in branch_data:
                branch_related_data = branch['fields']
                branch_related_data.update({'ifsc': branch['pk']})
                data.append(branch_related_data)
            autocomplete_data['branches'] = data
            return Response(data=autocomplete_data, status=200)
        except ValueError as e:
            return Response(data={'q': 'BranchName is required'}, status=400)
        except Exception as e:
            print("Exception %s"%e)
            return Response(status=500)


class AllPossibleMatch(APIView):

    def get(self, request):
        try:
            query_param = request.query_params.get('q', None)
            if not query_param:
                raise ValueError()
            fields = [f for f in Branches._meta.fields if isinstance(f, CharField)]
            queries_upper = [Q(**{f.name: query_param.upper()}) for f in fields]
            queries_lower = [Q(**{f.name: query_param.lower()}) for f in fields]
            qs = Q()
            for queryu, queryl in zip(queries_upper,queries_lower):
                qs = qs | queryu
                qs = qs | queryl
            limit = request.query_params.get('limit', 3)
            offset = request.query_params.get('offset', 0)
            bb = Branches.objects.filter(qs).order_by('-ifsc')[int(offset):int(limit)]
            branch_data = serializers.serialize("json", bb)
            branch_data = json.loads(branch_data)
            autocomplete_data = {}
            data = []
            for branch in branch_data:
                branch_related_data = branch['fields']
                branch_related_data.update({'ifsc': branch['pk']})
                data.append(branch_related_data)
            autocomplete_data['branches'] = data
            return Response(data=autocomplete_data, status=200)
        except ValueError as e:
            return Response(data={'q': 'Query param is required'}, status=400)
        except Exception as e:
            print("Exception %s" % e)
            return Response(status=500)
