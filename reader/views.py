from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import PyPDF2
from django import forms
import requests
from textwrap import wrap
import ast, json
# Create your views here.
class FileInputForm(forms.Form):
    file = forms.FileField()
def pdftotext(f):
    pdfReader = PyPDF2.PdfReader(f)
    numpages = pdfReader.numPages
    text = ""
    for i in range(1, numpages+1):
        pageobj = pdfReader.getPage(i-1)
        text += pageobj.extract_text()
    text.replace(';','\n')
    return text
    
def index(request):
    if request.method == 'POST':
        form = FileInputForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
        text = pdftotext(file)
        read_text = text
        if request.POST.get('type') == 'nv':
            url = 'https://viettelgroup.ai/voice/api/tts/v1/rest/syn'
            headers = {'Content-type': 'application/json', 'token': '9R-ER2eOy-wntRlF08gBivjyvVvxFGG3IKCT9CldmW3nYtbXkThd45gd2U3lTUt6'}
            data = {"text":read_text, "voice":"hn-phuongtrang", "without_filter":False, "tts_return_option":3}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            f = open("reader/static/reader/audio.mp3", 'wb')
            f.write(response.content)
            f.close()
            return render(request, "reader/reader.html", {
                "text":text
            })
        else:
            return render(request, "reader/reader.html", {
            "text":text,
            "read_text":read_text,
            
            })
    else:
        return render(request, "reader/index.html", {
            "form":FileInputForm
        })
def test(request):
    return render(request, "reader/test_reader.html")