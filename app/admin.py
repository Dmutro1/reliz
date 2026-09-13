from django.contrib import admin
from .models import Category, Tag, Author, Mod, TexturePack, Modpack, World, Shader


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name', 'email')


@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'category', 'game_version', 'downloads', 'is_published', 'created_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'description')
    filter_horizontal = ('tags',)


@admin.register(TexturePack)
class TexturePackAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'category', 'game_version', 'downloads', 'is_published', 'created_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'description')
    filter_horizontal = ('tags',)


@admin.register(Modpack)
class ModpackAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'category', 'game_version', 'downloads', 'is_published', 'created_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'description')
    filter_horizontal = ('tags',)


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'category', 'game_version', 'downloads', 'is_published', 'created_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'description')
    filter_horizontal = ('tags',)


@admin.register(Shader)
class ShaderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'category', 'game_version', 'downloads', 'is_published', 'created_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'description')
    filter_horizontal = ('tags',)
