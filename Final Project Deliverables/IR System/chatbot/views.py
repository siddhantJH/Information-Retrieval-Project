from django.shortcuts import render
from django.http import JsonResponse
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
        print(para_phrases)
        idx = random.randint(0,len(para_phrases)-1)
        response = para_phrases[idx][0]
        return JsonResponse({'response': response})
    return render(request, 'chatbot.html')