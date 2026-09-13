from django.core.management.base import BaseCommand
from django.utils.text import slugify

from app.models import Author, Category, Mod, Tag


MODS = [
    ('Iris Shaders', 'coderbot', 'A modern shader pack loader for Minecraft intended to be compatible with existing OptiFine shader packs', 'Optimization', ['Fabric', 'NeoForge', 'Quilt'], 171290000),
    ('Cloth Config API', 'shedaniel', 'Configuration library for Minecraft Mods', 'Library', ['Fabric', 'Forge', 'NeoForge'], 163420000),
    ('Entity Culling', 'tr7zw', 'Using async path-tracing to hide Block-Entities that are not visible', 'Optimization', ['Fabric', 'Forge', 'NeoForge', 'Babric'], 161860000),
    ('FerriteCore', 'malte0811', 'Memory usage optimizations for Minecraft', 'Optimization', ['Fabric', 'Forge', 'NeoForge'], 147040000),
    ('Mod Menu', 'Terraformers', 'Adds a mod menu to view the list of mods you have installed.', 'Utility', ['Fabric', 'Quilt'], 140010000),
    ('Lithium', 'CaffeineMC', 'No-compromises game logic optimization mod, useful for single-player and multiplayer servers.', 'Optimization', ['Fabric', 'NeoForge', 'Quilt'], 124470000),
    ('ImmediatelyFast', 'RaphiMC', 'Speed up immediate mode rendering in Minecraft', 'Optimization', ['Fabric', 'Forge', 'NeoForge', 'Quilt'], 120230000),
    ('YetAnotherConfigLib (YACL)', 'isxander', 'A builder-based configuration library for Minecraft!', 'Library', ['Fabric', 'Forge'], 119040000),
    ('Fabric Language Kotlin', 'modmuss50', 'Enables usage of the Kotlin programming language for Fabric mods.', 'Library', ['Fabric'], 114550000),
    ("Xaero's Minimap", 'xaero96', 'Displays a map of the nearby world terrain, players, mobs, and entities.', 'Adventure', ['Fabric', 'Forge'], 107180000),
    ('Architectury API', 'architectury', 'An intermediary API aimed to ease developing multiplatform mods.', 'Library', ['Fabric', 'Forge', 'NeoForge', 'Quilt'], 97070000),
]


class Command(BaseCommand):
    help = 'Add sample Minecraft mods to the catalog.'

    def handle(self, *args, **options):
        image_names = ['mods/icon.png', 'mods/fabric-api.png', 'mods/295862f4724dc3f78df3447ad6072b2dcd3ef0c9_96.webp']
        created_count = 0

        for index, (title, author_name, summary, category_name, loader_names, downloads) in enumerate(MODS):
            author, _ = Author.objects.get_or_create(name=author_name)
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)},
            )
            mod, created = Mod.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title,
                    'summary': summary,
                    'game_version': '1.21.1',
                    'downloads': downloads,
                    'author': author,
                    'category': category,
                    'image': image_names[index % len(image_names)],
                },
            )
            if created:
                mod.tags.set([
                    Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name)})[0]
                    for name in loader_names
                ])
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Added {created_count} new mods. Total: {Mod.objects.count()}'))
