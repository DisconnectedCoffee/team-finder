from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Project, Skill
from .forms import ProjectForm
from django.core.paginator import Paginator


def project_list_view(request):
    """Главная страница со списком проектов, пагинацией и фильтрацией по навыкам (Вариант 3)."""
    skill_filter = request.GET.get("skill")
    projects_list = Project.objects.all().order_by("-created_at")

    if skill_filter:
        projects_list = projects_list.filter(skills__name=skill_filter)

    paginator = Paginator(projects_list, 12)
    page_number = request.GET.get("page")
    projects = paginator.get_page(page_number)

    all_skills = Skill.objects.all().order_by("name")

    return render(request, "projects/project_list.html", {
        "projects": projects,
        "all_skills": all_skills,
        "active_skill": skill_filter,
    })


def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project_view(request):
    """Создание нового проекта"""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect("projects:project_detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project_view(request, pk):
    """Редактирование существующего проекта"""
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user and not request.user.is_staff:
        return redirect("projects:project_detail", pk=project.pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:project_detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required
@require_POST
def complete_project_view(request, pk):
    """Завершение проекта владельцем"""
    project = get_object_or_404(Project, pk=pk)
    if project.owner == request.user and project.status == "open":
        project.status = "closed"
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})
    return JsonResponse({"status": "error"}, status=400)


@login_required
@require_POST
def toggle_participate_view(request, pk):
    """Присоединение/отказ от участия в проекте"""
    project = get_object_or_404(Project, pk=pk)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({"status": "ok"})


def skills_autocomplete(request):
    """Автодополнение навыков"""
    query = request.GET.get("q", "")
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[:10]
    data = [{"id": s.id, "name": s.name} for s in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def add_project_skill(request, pk):
    """Добавление навыка к проекту"""
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return JsonResponse({"error": "Forbidden"}, status=403)

    skill_id = request.POST.get("skill_id")
    name = request.POST.get("name")

    created = False
    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())
    else:
        return JsonResponse({"error": "Invalid data"}, status=400)

    if skill not in project.skills.all():
        project.skills.add(skill)
        added = True
    else:
        added = False

    return JsonResponse({
        "skill_id": skill.id,
        "created": created,
        "added": added
    })


@login_required
@require_POST
def remove_project_skill(request, pk, skill_id):
    """Удаление навыка у проекта"""
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return JsonResponse({"error": "Forbidden"}, status=403)
    skill = get_object_or_404(Skill, pk=skill_id)
    project.skills.remove(skill)
    return JsonResponse({"status": "ok"})
