from django.http import Http404
from django.shortcuts import redirect, render

from .models import Comment, Mod, TexturePack, Modpack, World, Shader, Tag, User, Profile
from .models import Category
from .forms import CommentForm, ProfileForm
from django.utils.text import slugify
import re
from rest_framework.generics import *
from .serializers import ModSerializer, TexturePackSerializer, ModpackSerializer, WorldSerializer, ShaderSerializer
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.core.paginator import Paginator
from django.utils import timezone


# The homepage shows one rotating item for each content type.
def home(request):
    hour_index = int(timezone.now().timestamp() // 3600)

    def featured_item(model, offset):
        items = list(model.objects.order_by('-created_at'))
        if not items:
            return []
        return [items[(hour_index + offset) % len(items)]]

    context = {
        'mods': featured_item(Mod, 0),
        'texture_packs': featured_item(TexturePack, 1),
        'modpacks': featured_item(Modpack, 2),
        'worlds': featured_item(World, 3),
        'shaders': featured_item(Shader, 4),
    }
    return render(request, 'homepage.html', context)


# The profile is restricted to authenticated users and supports avatar changes.
@login_required(login_url=reverse_lazy('login'))
def profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile_user': request.user, 'profile_form': form, 'user_profile': user_profile})


# Shared view for lists of mods, worlds, shaders, and other content.
def content_list(request, model_name):
    model_map = {
        'mods': {
            'model': Mod,
            'title': 'Mods',
            'empty_message': 'No mods yet.',
        },
        'texture-packs': {
            'model': TexturePack,
            'title': 'Texture Packs',
            'empty_message': 'No texture packs yet.',
        },
        'modpacks': {
            'model': Modpack,
            'title': 'Modpacks',
            'empty_message': 'No modpacks yet.',
        },
        'worlds': {
            'model': World,
            'title': 'Worlds',
            'empty_message': 'No worlds yet.',
        },
        'shaders': {
            'model': Shader,
            'title': 'Shaders',
            'empty_message': 'No shaders yet.',
        },
    }

    page = model_map.get(model_name)
    if not page:
        raise Http404('Page not found.')

    # Support multiple versions and loaders through repeated GET parameters.
    versions_selected = request.GET.getlist('version')
    show_all_versions = request.GET.get('show_all_versions') == '1'
    loaders_selected = request.GET.getlist('loader')

    # Use the first selected version for the description.
    current_version = versions_selected[0] if versions_selected else ''

    # Merge database versions with the built-in Minecraft version list.
    db_versions = list(
        page['model'].objects
        .exclude(game_version='')
        .values_list('game_version', flat=True)
        .distinct()
    )

    fixed_versions = ['26.2', '26.1.2', '26.1.1', '26.1']

    # Keep common releases available even when the database is empty.
    minecraft_versions = [
        '1.21.1', '1.21', '1.20.2', '1.20.1', '1.20',
        '1.19.4', '1.19.3', '1.19.2', '1.19.1', '1.19',
        '1.18.2', '1.18.1', '1.18', '1.17.1', '1.17',
        '1.16.5', '1.16.4', '1.15.2', '1.12.2', '1.8.9', '1.0'
    ]

    # Remove duplicates while preserving first-seen order.
    combined = []
    for v in (fixed_versions + minecraft_versions + db_versions):
        if v and v not in combined:
            combined.append(v)

    def version_key(v):
        nums = re.findall(r"\d+", v)
        try:
            parts = [int(x) for x in nums]
        except ValueError:
            parts = [0]
        # Normalize versions to three parts for stable sorting.
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts)

    # Show newer versions first.
    version_values = sorted(combined, key=lambda x: version_key(x), reverse=True)

    # Human-readable version descriptions for the filter information panel.
    version_descriptions = {
        '26.2': '26.2 (Chaos Cubed) — sulfur caves and cubes.',
        '26.1': '26.1 (Tiny Takeover) — updated baby mobs.',
        '1.21': '1.21 (Tricky Trials) — trial chambers and challenges.',
        '1.20': '1.20 (Trails & Tales) — archaeology and the sniffer.',
        '1.19': '1.19 (The Wild Update) — deep darkness and the Warden.',
        '1.18': '1.18 (Caves & Cliffs: Part II) — new mountain generation.',
        '1.17': '1.17 (Caves & Cliffs: Part I) — axolotls and amethyst.',
        '1.16': '1.16 (Nether Update) — a complete Nether overhaul.',
        '1.15': '1.15 (Buzzy Bees) — bees and beehives.',
        '1.14': '1.14 (Village & Pillage) — village updates and pillagers.',
        '1.13': '1.13 (Update Aquatic) — dolphins, coral, and oceans.',
        '1.12': '1.12 (World of Color Update) — colorful concrete and parrots.',
        '1.11': '1.11 (Exploration Update) — woodland mansions and llamas.',
        '1.10': '1.10 (Frostburn Update) — polar bears and icy biomes.',
        '1.9': '1.9 (Combat Update) — a new combat system and Elytra.',
        '1.8': '1.8 (Bountiful Update) — ocean monuments and guardians.',
        '1.7': '1.7 (The Update that Changed the World) — new biomes.',
        '1.6': '1.6 (Horse Update) — horses and leads.',
        '1.5': '1.5 (Redstone Update) — hoppers, comparators, and quartz.',
        '1.4': '1.4 (Pretty Scary Update) — witches, bats, and the Wither.',
        '1.3': '1.3 — trading with villagers.',
        '1.2': '1.2 — iron golems and jungles.',
        '1.1': '1.1 — superflat worlds and spawn eggs.',
        '1.0': '1.0 (Official Release) — the End dimension and the dragon.'
    }

    current_description = version_descriptions.get(current_version, '')

    # Known loaders use a fixed order; other tags follow them.
    preferred_loaders = ['Fabric', 'Forge', 'NeoForge', 'Babric', 'BTA (Babric)', 'Java Agent', 'Legacy Fabric', 'LiteLoader', "Risugami's ModLoader", 'NilLoader', 'Ornithe', 'Quilt', 'Rift']
    environment_values = ['Client', 'Server']
    # Create standard tags so they remain available in filters without content.
    def ensure_tag(name):
        try:
            return Tag.objects.get(name=name)
        except Tag.DoesNotExist:
            base_slug = slugify(name)[:50]
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return Tag.objects.create(name=name, slug=slug)

    for name in preferred_loaders + environment_values:
        if not Tag.objects.filter(name=name).exists():
            ensure_tag(name)

    loader_values = [name for name in preferred_loaders if Tag.objects.filter(name=name).exists()]
    other_tags = list(Tag.objects.exclude(name__in=loader_values + environment_values).values_list('name', flat=True).distinct().order_by('name'))
    loader_values.extend(other_tags)

    environment_selected = request.GET.getlist('environment')

    # Sidebar categories are also created automatically when needed.
    categories_selected = request.GET.getlist('category')

    desired_categories = [
        'Adventure', 'Cursed', 'Decoration', 'Economy', 'Equipment', 'Food',
        'Game Mechanics', 'Library', 'Magic', 'Management', 'Minigame', 'Mobs',
        'Optimization', 'Social', 'Storage', 'Technology', 'Transportation', 'Utility', 'World Generation'
    ]

    def ensure_category(name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            base_slug = slugify(name)[:100]
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return Category.objects.create(name=name, slug=slug)

    for cname in desired_categories:
        if not Category.objects.filter(name=cname).exists():
            ensure_category(cname)

    categories_qs = list(Category.objects.all().order_by('name'))

    category_icons_map = {
        'Adventure': '🧭', 'Cursed': '👻', 'Decoration': '🏠', 'Economy': '💲', 'Equipment': '🛡️',
        'Food': '🍖', 'Game Mechanics': '⚙️', 'Library': '📚', 'Magic': '✨', 'Management': '🗂️',
        'Minigame': '🎯', 'Mobs': '🐾', 'Optimization': '⚡', 'Social': '💬', 'Storage': '📦',
        'Technology': '🔧', 'Transportation': '🚚', 'Utility': '🧰', 'World Generation': '🌍'
    }

    categories = []
    for cat in categories_qs:
        icon = category_icons_map.get(cat.name, '▫️')
        categories.append({'name': cat.name, 'slug': cat.slug, 'icon': icon})

    items = page['model'].objects.all()
    if versions_selected and not show_all_versions:
        items = items.filter(game_version__in=versions_selected)

    if loaders_selected:
        items = items.filter(tags__name__in=loaders_selected).distinct()

    if environment_selected:
        items = items.filter(tags__name__in=environment_selected).distinct()

    if categories_selected:
        items = items.filter(category__slug__in=categories_selected)

    # Show newest content first by default.
    items = items.order_by('-created_at')
    items_page = Paginator(items, 12).get_page(request.GET.get('page'))
    pagination_query = request.GET.copy()
    pagination_query.pop('page', None)

    context = {
        'items': items_page,
        'page_obj': items_page,
        'pagination_query': pagination_query.urlencode(),
        'title': page['title'],
        'empty_message': page['empty_message'],
        'model_name': model_name,
        'versions': version_values,
        'current_versions': versions_selected,
        'current_version': ', '.join(versions_selected) if versions_selected else '',
        'show_all_versions': show_all_versions,
        'current_version_description': current_description,
        
        'loaders': loader_values,
        'current_loaders': loaders_selected,
        'current_loader': loaders_selected[0] if loaders_selected else '',
        'environment_values': environment_values,
        'current_environments': environment_selected,
        'current_environment': ', '.join(environment_selected) if environment_selected else '',
        'categories': categories,
        'current_categories': categories_selected,
        'current_category': ', '.join(categories_selected) if categories_selected else '',
    }
    return render(request, 'content_list.html', context)


def detail_view(request, model_name, slug):
    model_map = {
        'mods': Mod,
        'texture-packs': TexturePack,
        'modpacks': Modpack,
        'worlds': World,
        'shaders': Shader,
    }
    
    model = model_map.get(model_name)
    if not model:
        raise Http404('Page not found.')
    
    try:
        item = model.objects.get(slug=slug)
    except model.DoesNotExist:
        raise Http404(f'{model_name} not found.')
    
    # Increment the view counter when a content page is opened.
    item.views += 1
    item.save(update_fields=['views'])

    comments = Comment.objects.none()
    comments_page = None
    comment_form = None
    if model_name == 'mods':
        comments = item.comments.select_related('user').all()
        comments_page = Paginator(comments, 5).get_page(request.GET.get('comments_page'))
        comment_form = CommentForm()

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")

            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.mod = item
                comment.user = request.user
                comment.save()
                return redirect(request.path)
    
    context = {
        'item': item,
        'model_name': model_name,
        'comments': comments,
        'comments_page': comments_page,
        'comment_form': comment_form,
    }
    return render(request, 'detail.html', context)

# API endpoints for retrieving and editing content.
class ModListApiView(ListCreateAPIView):
    queryset = Mod.objects.all()
    serializer_class = ModSerializer
class TexturePackListApiView(ListCreateAPIView):
    queryset = TexturePack.objects.all()
    serializer_class = TexturePackSerializer
class ModpackListApiView(ListCreateAPIView):
    queryset = Modpack.objects.all()
    serializer_class = ModpackSerializer
class WorldListApiView(ListCreateAPIView):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
class ShaderListApiView(ListCreateAPIView):
    queryset = Shader.objects.all()
    serializer_class = ShaderSerializer
class ModDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Mod.objects.all()
    serializer_class = ModSerializer
class TexturePackDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = TexturePack.objects.all()
    serializer_class = TexturePackSerializer
class ModpackDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Modpack.objects.all()
    serializer_class = ModpackSerializer
class WorldDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
class ShaderDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Shader.objects.all()
    serializer_class = ShaderSerializer

# Login, logout, and user registration.
class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        # Keep direct GET logout links from older templates working.
        return self.post(request, *args, **kwargs)

class UserRegisterView(CreateView):
    model = User
    form_class = UserCreationForm 
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)