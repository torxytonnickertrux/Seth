from django.db import models

class UserRequest(models.Model):
    client_ip = models.GenericIPAddressField()  # IP do cliente
    forwarded_ip = models.GenericIPAddressField(null=True, blank=True)  # IP do proxy (se existir)
    user_agent = models.TextField()  # Dados do navegador
    cookies = models.JSONField()  # Cookies enviados
    headers = models.JSONField()  # Todos os cabeçalhos
    query_params = models.JSONField()  # Parâmetros GET
    post_data = models.JSONField()  # Dados POST
    geolocation = models.JSONField(null=True, blank=True)  # Geolocalização (opcional)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp de criação

    def __str__(self):
        return f"IP: {self.client_ip}, User-Agent: {self.user_agent[:50]}"