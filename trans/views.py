from django.shortcuts import render
import googletrans
from googletrans import Translator
# Create your views here.

def index(req):
    context={
        "nd":googletrans.LANGUAGES
    }
    if req.method == "POST":
        i = req.POST.get("intrans")
        insec = req.POST.get("insec", "")
        outsec = req.POST.get("outsec", "")
        translator = Translator()
        o = translator.translate(i, src=insec, dest=outsec)
        print(o)
        context.update({
            "o":o.text,
            "insec":insec,
            "outsec":outsec,
            "i":i,
        })
    return render(req, "trans/index.html",context)