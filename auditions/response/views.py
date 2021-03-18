from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, response


from .models import Question,Response
from accounts.models import Profile

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    return render(request,'response/index.html')

@login_required(login_url='/accounts/login/')
def get_question(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    try:
        question = Question.objects.get(ques_round = profile.curr_round)
    except:
        if(profile.curr_round > 37):
            return render(request,'response/end.html')
    if(request.method == 'POST'):
        response = Response(profile = profile)
        response.question = question
        response.response = request.POST["response"] ##Assuming form input name = response
        response.save()
        profile.curr_round += 1
        profile.save()
        return redirect('get-question')
    time_data = profile.get_completion_time()
    if(question.question_type == 'N'):
        return render(request,'response/get_question.html',{'question':question,'time':time_data})
    elif(question.question_type == 'I'):
        return render(request,'response/get_question_image.html',{'question':question,'time':time_data})

def timer_expired(request):
    profile = Profile.objects.get(user = request.user) 
    profile.completed= True
    profile.save()
    return render(request,'response/end.html')

def questions(request):
    user= request.user
    
    profile = Profile.objects.get(user = user)
    
    question=Question.objects.all()
    questionlist=[]
    for i in question:
        questionlist.append({
            'round':i.ques_round,
            'text':i.text,
            'type':i.question_type,
            'image':i.image,
        })
    if request.method=='POST':
        answer=request.POST
    
        for i in question:
            #question=Question.objects.get(ques=i.ques_round)
            responses =Response.objects.create(profile=profile, question=i)
            responses.response=answer[str(i.ques_round)]
            responses.save()

        profile.completed = True
        profile.save()
        return render(request, 'response/end.html')
    
    if profile.completed==True:
        return render(request,'response/end.html')
    time_data = profile.get_completion_time()
    
    return render(request,'response/q2.html', {'questionlist':questionlist, 'user':user,'time':time_data})

