from django.db import models


# ## Model Managers ## #
class ArticleManager(models.Manager):
    def all(self):
        qs = super(ArticleManager, self).all()
        return qs

    def published(self):
        qs = super(ArticleManager, self).filter(draft=False)
        return qs

    def visible(self):
        qs = super(ArticleManager, self).filter(draft=False).filter(visible=True)
        return qs

    def recent_five(self):
        qs = super(ArticleManager, self).filter(draft=False).filter(visible=True).order_by('-date_added')[:5]
        return qs


class CategoryManager(models.Manager):
    def all(self):
        qs = super(CategoryManager, self).all()
        return qs

    def active(self, group_id):
        qs = super(CategoryManager, self).filter(active=True)
        return qs


class RefManager(models.Manager):
    def all(self):
        qs = super(RefManager, self).all()
        return qs

    def primary(self):
        qs = super(RefManager, self).order_by('primary')[:1]
        return qs


class ServicesManager(models.Manager):
    def all(self):
        qs = super(ServicesManager, self).all()
        return qs

    def top_five(self):
        qs = super(ServicesManager, self).order_by('priority')[:5]
        return qs


class TagManager(models.Manager):
    def all(self):
        qs = super(TagManager, self).all()
        return qs

    def active(self):
        qs = super(TagManager, self).filter(active=True)
        return qs


class CustomerManager(models.Manager):
    def all(self):
        qs = super(CustomerManager, self).all()
        return qs

    def active(self):
        qs = super(CustomerManager, self).filter(active=True)
        return qs


class FeatureManager(models.Manager):
    def all(self):
        qs = super(FeatureManager, self).all()
        return qs

    def active(self):
        qs = super(FeatureManager, self).filter(active=True)
        return qs


class SkillManager(models.Manager):
    def all(self):
        qs = super(SkillManager, self).all()
        return qs

    def active(self):
        qs = super(SkillManager, self).filter(active=True)
        return qs


# ## Models ## #

class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    active = models.BooleanField(default=True)
    objects = TagManager()

    def __str__(self):
        return self.tag.title()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    objects = CategoryManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class Article(models.Model):
    author = models.CharField(max_length=100, unique=False)
    caption = models.CharField(max_length=50, unique=False)
    extract = models.CharField(max_length=300)
    story = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    draft = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    image_file = models.FileField(upload_to='blog_image', blank=True, null=True)
    article_file = models.FileField(upload_to='blog_article', blank=True, null=True)
    project = models.BooleanField(default=False)
    objects = ArticleManager()

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.caption.title()


class Reference(models.Model):
    company = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    primary = models.IntegerField(null=False, unique=True)
    objects = RefManager()

    def __str__(self):
        return self.company.title()


class Services(models.Model):
    service = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    priority = models.IntegerField(null=False, unique=True)
    image_file = models.FileField(upload_to='service_icon', blank=True, null=True)
    descrip = models.CharField(max_length=300, blank=True, null=True)
    objects = ServicesManager()

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.service.title()


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sector = models.CharField(max_length=50, unique=False, blank=True, null=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    image_file = models.FileField(upload_to='service_icon', blank=True, null=True)
    descrip = models.CharField(max_length=300, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = CustomerManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title() or self.sector.title()


class Feature(models.Model):
    feature = models.CharField(max_length=50, unique=True)
    image_file = models.FileField(upload_to='feature_icon', blank=True, null=True)
    descrip = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = FeatureManager()

    class Meta:
        ordering = ['feature']

    def __str__(self):
        return self.feature.title()


class Skill(models.Model):
    skill = models.CharField(max_length=50, unique=True)
    descrip = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = SkillManager()

    class Meta:
        ordering = ['skill']

    def __str__(self):
        return self.skill.title()
