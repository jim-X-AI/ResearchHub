from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.
from .models import Topic, Entry, LearningEntry
from .forms import TopicForm, EntryForm, LearningEntryForm
from django.http import HttpResponseForbidden


# def index(request):
#     """The home page for learning log"""
#     return render(request, 'learning_logs/index.html')


# noinspection PyShadowingNames
@login_required
def topics(request):
    """This shows all the topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


# noinspection PyShadowingNames
@login_required
def topic(request, topic_id):
    """This shows individual topic with their entries"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date')
    context = {
        'topic': topic,
        'entries': entries,
    }

    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Adds a new topic"""
    if request.method != 'POST':
        """no data is submitted"""
        form = TopicForm()
    else:
        # Post data submitted
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Displays a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


# noinspection PyShadowingNames
@login_required
def new_entry(request, topic_id):
    """To add new entries"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        """No entry entered"""
        form = EntryForm()
    else:
        """Wants to enter an entry"""
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
        return redirect('learning_logs:topic', topic_id=topic.id)
    context = {
        'topic': topic,
        'form': form,
    }
    # Display a blank or invalid form
    return render(request, 'learning_logs/new_entry.html', context)


# noinspection PyShadowingNames
@login_required
def edit_entry(request, entry_id):
    """To edit already existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def share_learning(request):
    if request.method == 'POST':
        form = LearningEntryForm(request.POST)
        if form.is_valid():
            learning_entry = form.save(commit=False)
            learning_entry.user = request.user
            learning_entry.save()
            return redirect('learning_logs:learning_entries')
    else:
        form = LearningEntryForm()
    context = {'form': form}
    return render(request, 'learning_logs/share_learning.html', context)

@login_required
def learning_entries(request):
    entries = LearningEntry.objects.all().order_by('date')
    context = {'entries': entries}
    return render(request, 'learning_logs/learning_entries.html', context)




@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')  # Redirect to the topics list after saving
    else:
        form = TopicForm(instance=topic)
    return render(request, 'learning_logs/edit_topic.html', {'form': form, 'topic': topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    return render(request, 'learning_logs/delete_topic.html', {'topic': topic})
