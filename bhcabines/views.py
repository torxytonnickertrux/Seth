from django.shortcuts import render

import logging
import requests
from django.http import JsonResponse
from django.utils.html import escape
from .models import UserRequest
from django.http import JsonResponse, HttpResponseNotAllowed

logging.basicConfig(
    filename='request_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def geolocate_ip(ip):
    """Enriquece os dados do IP com geolocalização."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return {}

def capture_request_data(request):
    if request.method == 'POST':
        # Captura os dados principais
        headers = {k: escape(v) for k, v in request.headers.items()}
        client_ip = request.META.get('REMOTE_ADDR')
        forwarded_ip = request.headers.get('X-Forwarded-For', client_ip)
        user_agent = escape(request.headers.get('User-Agent', 'Unknown'))
        cookies = {k: escape(v) for k, v in request.COOKIES.items()}
        query_params = {k: escape(v) for k, v in request.GET.items()}
        post_data = {k: escape(v) for k, v in request.POST.items()}
        geolocation = geolocate_ip(forwarded_ip)

        # Prevenção de duplicação com base em IP e User-Agent
        existing_user = UserRequest.objects.filter(client_ip=client_ip, user_agent=user_agent).first()

        if not existing_user:
            # Cria um novo registro
            user_request = UserRequest.objects.create(
                client_ip=client_ip,
                forwarded_ip=forwarded_ip,
                user_agent=user_agent,
                cookies=cookies,
                headers=headers,
                query_params=query_params,
                post_data=post_data,
                geolocation=geolocation,
            )
            logging.info(f"Novo usuário salvo: {user_request}")
            return JsonResponse({"message": "Usuário registrado com sucesso.", "data": user_request.id})
        else:
            # Responde caso o registro já exista
            logging.info(f"Usuário já existe: {existing_user}")
            return JsonResponse({"message": "Usuário já registrado.", "data": existing_user.id})
    elif request.method == 'GET':
        # Retorna uma mensagem clara para requisições GET
        return JsonResponse({"message": "Endpoint ativo. Use POST para enviar dados."})
    else:
        # Responde com "Método não permitido" para outros métodos
        return HttpResponseNotAllowed(['POST'])

# Create your views here.
def home(request):
    return render(request, 'bhcabines/index.html')
