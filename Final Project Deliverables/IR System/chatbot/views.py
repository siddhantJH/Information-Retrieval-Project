from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import markdown
from . import llm
from . import paraphraser
import random

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = llm.ask_Query(message)
        response = markdown.markdown(response)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


def paraphrase(request):
    if request.method == 'POST':
        para_phrases = paraphraser.parrot.augment(input_phrase=request.POST.get('message'))
        index=0
        if(para_phrases!=None):
            index = random.randint(0,len(para_phrases)-1)
        else:
            index=0
        response = para_phrases[index][0]
        if(response == None):
            return HttpResponse('<h1>Page not found</h1>', status_code='404')
        return JsonResponse({'response': response})
    return render(request, 'chatbot.html')
