from django.shortcuts import render
from django.http import JsonResponse
from . import llm
def chatbot(request):
    #chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        #response = "Hi"
        response = llm.ask_Query(message)
        #chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        #chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')