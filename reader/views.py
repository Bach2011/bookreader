from http.client import HTTPResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import PyPDF2
# Create your views here.
def index(request):
    if request.method == 'POST':
        path = request.POST.get('location')
        lang = request.POST.get('lang')
        pdfReader = PyPDF2.PdfReader(path)
        numpages = pdfReader.numPages
        text = ""
        for i in range(1,numpages+1):
            pageobj = pdfReader.getPage(i-1)
            text += pageobj.extract_text()
        return render(request, "reader/reader.html", {
            "text":text,
            "lang":lang
        })
    else:
        return render(request, "reader/index.html")
