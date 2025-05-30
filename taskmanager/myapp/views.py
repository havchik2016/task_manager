from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from .models import Task, Project, User
from .forms import TaskForm, UserForm, FilterForm, ProjectForm

current_user = "user1"
priority_filter = "None"
status_filter = "None"
projects = set()
user_projects = dict()
admins = dict()
# Create your views here.


def index(request):
    return render(request, 'HelloWorld/index.html')



def task_list_view(request):
    global current_user, priority_filter, status_filter, user_projects, projects, last_project
    tasks = Task.objects.all()
    obj_projects = Project.objects.all()
    form = TaskForm(request.POST or None)
    userform = UserForm(request.POST or None)
    filterform = FilterForm(request.POST or None)
    projectform = ProjectForm(request.POST or None)

    if form.is_valid():
        task = form.save()
        task.user = current_user
        if task.project not in user_projects[current_user]:
            task.delete()
            return redirect('task_list')
        if request.htmx:
            return render(request, 'partials/task_item.html', {'task': task})
        return redirect('task_list')

    if userform.is_valid():
        user_object = userform.save()
        current_user = user_object.user
        return redirect('task_list')

    if filterform.is_valid():
        filter_object = filterform.save()
        priority_filter = filter_object.priority_filter
        status_filter = filter_object.status_filter
        return redirect('task_list')

    if projectform.is_valid():
        project = projectform.save()
        if project.project_name in projects:
            project.delete()
        else:
            last_project = project
            projects.add(project.project_name)
            admins[project.project_name] = {current_user}
            if current_user not in user_projects:
                user_projects[current_user] = {project.project_name}
            else:
                user_projects[current_user].add(project.project_name)
        return redirect('task_list')

    return render(request, 'task_list.html', {'tasks': tasks, 'form': form, 'userform': userform,
                                              'filterform': filterform, 'current_user': current_user,
                                              'projectform': projectform, 'projects': obj_projects,
                                              'current': user_projects.get(current_user, set()),
                                              'priority_filter': priority_filter, 'status_filter': status_filter})


def task_edit_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'partials/task_item.html', {'task': task})

    return render(request, 'partials/edit_task_form.html', {'form': form, 'task': task})


def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return HttpResponse('')


def project_edit_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if current_user not in admins.get(project.project_name, set()):
        return render(request, 'partials/project_item.html',
                      {'project': project, 'admins': admins[project.project_name],
                       'current_user': current_user})
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'partials/project_item.html', {'project': project, 'admins': admins[project.project_name],
                                                              'current_user': current_user})

    return render(request, 'partials/edit_project_form.html', {'form': form, 'project': project})


def add_user_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    print(project.project_name)
    userform = UserForm(request.GET or None, instance=User.create(current_user))
    if current_user not in admins.get(project.project_name, set()):
        return render(request, 'partials/project_item.html',
                      {'project': project, 'admins': admins[project.project_name],
                       'current_user': current_user})
    if request.method == 'POST' and userform.is_valid():
        obj = userform.save()
        user = obj.user
        user_projects[user].add(project.project_name)
        admins[project.project_name].add(user)
        return render(request, 'partials/project_item.html', {'project': project, 'admins': admins[project.project_name],
                                                              'current_user': current_user})

    return render(request, 'partials/add_user_form.html', {'form': userform})
