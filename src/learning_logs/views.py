from django.shortcuts import render
from .models import Topic,Entry
from .forms import TopicForm, EntryForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

def index(request):
    """home page for learning log"""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):

    """ show all the topics here."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request,topic_id):

    """ details of al entries regarding a topics """
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries': entries}
    return render(request,'learning_logs/topic.html',context)
    # to make sure request belongs to the valid user
    if topic.owner != request.user:
        raise Http404

@login_required
def new_topic(request):
    """ details regarding the new topic form"""
    if request.method != 'POST':
        #no data is submitted, generate an empty form
        form = TopicForm()
    else:
        #Submit button is clicked hence we need to verify if the entered data is valid
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

        
    #this means the entered form is invalid hence a display message
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html' , context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    """details regarding the new entry related to the topic"""
    if request.method != 'POST':
        #no data is submitted , generate an empty form
        form = EntryForm()
    
    else:
        #submit  button is clicked
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
            
        
    #if entry is invalid ence a display message
    context = {'topic': topic,'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request,entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # to make sure request belongs to the valid user
    if topic.owner != request.user:
        raise Http404

    """Detauls regarding editing an entry made"""
    if request.method != 'POST':
        #display the entry made here 
        form = EntryForm(instance=entry)
    else:
        #edit entry is submitted we need to replace the old entry by a new one
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    
    #if entry is invalid then we need to display message
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
