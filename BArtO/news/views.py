from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import News, NewsComment
from .forms import NewsCommentForm


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import NewsForm

UserModel = get_user_model()


@login_required
@permission_required('news.add_news', raise_exception=True)
def create_news(request):
    user = UserModel
    if request.user.role != 'editor':
        return redirect('permission_denied')  # Пренасочете, ако не е редактор
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('news:news_list')
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})


from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from .forms import NewsForm


@login_required
@permission_required('news.change_news', raise_exception=True)  # Проверка за разрешение
def edit_news(request, pk):
    # Вземане на новината по ID
    news_item = get_object_or_404(News, id=pk)

    # Ако потребителят е автор на новината или има разрешение за редактиране
    if request.user != news_item.author and not request.user.has_perm('news.change_news'):
        return redirect('news:news_list')  # Пренасочваме към списъка с новини, ако не е автор или няма право

    # Създаване на формата с текущото съдържание на новината
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()  # Записване на промените
            return redirect('news:news_detail',
                            pk=news_item.id)  # Пренасочване към детайлната страница на новината
    else:
        form = NewsForm(instance=news_item)

    return render(request, 'news/edit_news.html', {'form': form, 'news': news_item})


@login_required
@permission_required('news.delete_news', raise_exception=True)  # Проверка за разрешение
def delete_news(request, pk):
    # Вземане на новината по ID
    news_item = get_object_or_404(News, id=pk)

    # Ако потребителят не е автор на новината и няма разрешение за изтриване
    if request.user != news_item.author and not request.user.has_perm('news.delete_news'):
        return redirect('news:news_list')  # Пренасочваме към списъка с новини

    # Ако потребителят потвърди, че иска да изтрие новината
    if request.method == 'POST':
        news_item.delete()  # Изтриване на новината
        return redirect('news:news_list')  # Пренасочване към списъка с новини

    return render(request, 'news/delete_news.html', {'news': news_item})


class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news_list"
    ordering = ["-published_date"]
    paginate_by = 5


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"


class AddCommentView(LoginRequiredMixin, CreateView):
    model = NewsComment
    form_class = NewsCommentForm
    template_name = "news/add_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.news = get_object_or_404(News, id=self.kwargs["pk"])
        return super().form_valid(form)
