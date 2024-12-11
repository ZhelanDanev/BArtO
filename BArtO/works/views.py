from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Work
from .forms import WorkForm

@login_required
def work_list(request):
    # Вземи всички произведения
    works = Work.objects.all().order_by('-created_at')

    # Проверка дали има параметър за търсене по автор
    author_query = request.GET.get('author', '')  # Получаваме стойността на полето за търсене

    if author_query:
        # Ако има заявка за търсене по автор, филтрирай произведенията по автор
        works = works.filter(author__username__icontains=author_query)

    return render(request, 'works/work_list.html', {'works': works, 'author_query': author_query})

@login_required
def work_detail(request, pk):
    work = get_object_or_404(Work, pk=pk)
    return render(request, 'works/work_detail.html', {'work': work})

@login_required
def work_create(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.author = request.user
            work.save()
            return redirect('work_detail', pk=work.pk)
    else:
        form = WorkForm()
    return render(request, 'works/work_form.html', {'form': form})


@login_required
def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk)

    if request.user != work.author:
        return redirect('work_list')

    if request.method == 'POST':
        work.delete()
        return redirect('work_list')

    return render(request, 'works/work_delete.html', {'work': work})
