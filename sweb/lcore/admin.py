from django.contrib import admin

from .models import Services, Reference, Article, Category, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['caption', 'author', 'visible']

    class Meta:
        model = Article


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class RefAdmin(admin.ModelAdmin):
    list_display = ['company', 'primary']

    class Meta:
        model = Reference


admin.site.register(Reference, RefAdmin)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ['service', 'priority']

    class Meta:
        model = Services


admin.site.register(Services, ServicesAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'active']

    class Meta:
        model = Tag


admin.site.register(Tag, TagAdmin)
