from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def check_topic_owner(request, topic):
    """Не даёт пользователю открыть чужую тему."""
    if topic.owner != request.user:
        raise Http404


def index(request):
    """Домашняя страница приложения Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Выводит список тем текущего пользователя."""
    topics = (
        Topic.objects.filter(owner=request.user)
        .annotate(entries_count=Count('entry'))
        .order_by('date_added')
    )
    return render(request, 'learning_logs/topics.html', {'topics': topics})


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все её записи."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Добавляет новую тему."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            messages.success(request, 'Тема добавлена.')
            return redirect('learning_logs:topic', topic_id=new_topic.id)
    return render(request, 'learning_logs/new_topic.html', {'form': form})


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            messages.success(request, 'Запись добавлена.')
            return redirect('learning_logs:topic', topic_id=topic_id)
    return render(request, 'learning_logs/new_entry.html',
                  {'topic': topic, 'form': form})


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены.')
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
@require_POST
def delete_entry(request, entry_id):
    """Удаляет запись."""
    entry = get_object_or_404(Entry, id=entry_id)
    check_topic_owner(request, entry.topic)
    topic_id = entry.topic.id
    entry.delete()
    messages.success(request, 'Запись удалена.')
    return redirect('learning_logs:topic', topic_id=topic_id)


@login_required
@require_POST
def delete_topic(request, topic_id):
    """Удаляет тему вместе со всеми её записями."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    topic.delete()
    messages.success(request, 'Тема удалена.')
    return redirect('learning_logs:topics')
