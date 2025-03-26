from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm, ProfileUpdateForm,
    UserUpdateForm, PostForm, CommentForm
)
from .models import Profile, Post, Comment
from taggit.models import Tag


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required(login_url='blog:login')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'blog/profile.html', {'profile': profile})

@login_required(login_url='blog:login')
def profile_edit(request):
    # Get the current user's profile
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('blog:profile')  # Redirect to profile page after saving
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# ✅ ListView - Display all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Template: blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-published_date']  # Show newest posts first

    def get_queryset(self):
        # Prefetch the related tags for all posts in the queryset
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('tags')
        return queryset

# ✅ DetailView - Show individual blog posts
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Template for displaying post details

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Fetch all comments related to this post
        context['form'] = CommentForm()  # Include the comment form
        return context

# ✅ CreateView - Allow logged-in users to create posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # Template: blog/post_form.html
    success_url = reverse_lazy('blog:post-list')
    login_url = reverse_lazy('blog:login')

    def form_valid(self, form):
        # Automatically assign the logged-in user as the post author
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Handle tags after the post is saved
        self.handle_tags(form.cleaned_data.get('tags'))
        return response

    def handle_tags(self, tags):
        """Ensure all selected tags exist and associate them with the post."""
        for tag in tags:
            self.object.tags.add(tag)  # Add tag to post

# ✅ UpdateView - Allow only the author to edit posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # Reuse the same form template
    login_url = reverse_lazy('blog:login')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Allow only the post author to edit

    def form_valid(self, form):
        # Save the updated post
        response = super().form_valid(form)

        # Clear existing tags and add the newly selected tags
        self.object.tags.clear()
        self.handle_tags(form.cleaned_data.get('tags'))
        return response

    def handle_tags(self, tags):
        """Ensure all selected tags exist and associate them with the post."""
        for tag in tags:
            self.object.tags.add(tag)  # Add tag to post

# ✅ DeleteView - Allow only the author to delete posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Template: blog/post_confirm_delete.html
    success_url = reverse_lazy('blog:post-list')  # Redirect after deletion
    login_url = reverse_lazy('blog:login')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Allow only the post author to delete


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    login_url = reverse_lazy('blog:login')

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/edit_comment.html'  # Template: blog/edit_comment.html
    form_class = CommentForm
    login_url = reverse_lazy('blog:login')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Allow only the post author to edit

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.post.id})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/delete_comment.html'  # Template: blog/edit_comment.html
    login_url = reverse_lazy('blog:login')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Allow only the post author to edit

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.post.id})

class PostSearchView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Reuse the post list template
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass query to template
        return context

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Reuse the post list template
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)  # Get the tag object
        return Post.objects.filter(tags__in=[self.tag])  # Filter posts by tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag  # Pass the tag to the template
        return context