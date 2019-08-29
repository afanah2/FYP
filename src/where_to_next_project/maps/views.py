from django.views.generic import TemplateView
from maps.forms import InputForm
from django.shortcuts import render, redirect
from jsonrpc.proxy import ServiceProxy
from ast import literal_eval
from django.http import JsonResponse
import simplejson as json

s = ServiceProxy('http://localhost:8000/rpc/')

class HomeView(TemplateView):
    template_name = "maps/home.html"

    def get(self, request):
        context = {
            'title': 'Home',
        }

        return render(request, self.template_name, context)


    def post(self, request):
        print('post recieved maps view')
        data = request.POST
        print(data)
        if data['algorithm'] == 'heuristic':
            response = s.rpc.twice_around_the_tree(dict(data))
        else:
            response = s.rpc.branch_and_bound(dict(data))
        route = response['result']

        context = {
            'title': 'Results',
            'route': json.dumps(route)
        }

        return render(request, "maps/results.html", context)

class TestView(TemplateView):
    template_name = "maps/test.html"


    def get(self, request):
        context = {
            'title': 'Test Page',
        }

        return render(request, self.template_name, context)

    def post(self, request):
        print('post recieved maps view')
        data = request.POST
        print(data)
        if data['algorithm'] == 'heuristic':
            response = s.rpc.twice_around_the_tree(dict(data))
        else:
            response = s.rpc.branch_and_bound(dict(data))
        route = response['result']

        context = {
            'title': 'Results',
            'route': json.dumps(route),
            'test_mode': True
        }

        return render(request,  "maps/results.html", context)

class ResultsView(TemplateView):
    template_name = "maps/results.html"

    def get(self, request):
        context = {
            'title': 'Test Page'
        }
        
        return render(request, self.template_name, context)
