from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ContentItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_items')
    tags = models.ManyToManyField(Tag, blank=True, related_name='%(class)s_items')
    game_version = models.CharField(max_length=50, blank=True)
    downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Mod(ContentItem):
    image = models.ImageField(upload_to='mods/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Mod'
        verbose_name_plural = 'Mods'

    def get_absolute_url(self):
        return f'/mods/{self.slug}/'


class TexturePack(ContentItem):
    image = models.ImageField(upload_to='texture-packs/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Texture Pack'
        verbose_name_plural = 'Texture Packs'

    def get_absolute_url(self):
        return f'/texture-packs/{self.slug}/'


class Modpack(ContentItem):
    image = models.ImageField(upload_to='modpacks/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Modpack'
        verbose_name_plural = 'Modpacks'

    def get_absolute_url(self):
        return f'/modpacks/{self.slug}/'


class World(ContentItem):
    image = models.ImageField(upload_to='worlds/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'World'
        verbose_name_plural = 'Worlds'

    def get_absolute_url(self):
        return f'/worlds/{self.slug}/'


class Shader(ContentItem):
    image = models.ImageField(upload_to='shaders/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Shader'
        verbose_name_plural = 'Shaders'

    def get_absolute_url(self):
        return f'/shaders/{self.slug}/'
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} profile'


class Comment(models.Model):
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mod_comments')
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.mod.title}'