from django.db import models
from django_countries.fields import CountryField
from colorfield.fields import ColorField
from django.utils import timezone
from django.utils.timezone import now
from user_account.models import Code, License
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


class Client(models.Model):
    name = models.CharField(max_length=149, unique=True)
    slug = models.SlugField(max_length=149, default='my_name')
    picture = models.FileField(upload_to='pictures/', blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=149, unique=True)
    slug = models.SlugField(max_length=149, default='my_name')
    client = models.ForeignKey(Client, related_name='event_client', on_delete=models.CASCADE, blank=True,
                               null=True)  # default=1)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)  # date += datetime.timedelta(days=1)
    language = models.CharField(max_length=149, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    event_logo = models.FileField(upload_to='pictures/', blank=True, null=True)
    event_banner_1 = models.FileField(upload_to='pictures/', blank=True, null=True)
    event_banner_2 = models.FileField(upload_to='pictures/', blank=True, null=True)
    have_live_player = models.BooleanField(default=False)
    have_chat = models.BooleanField(default=False)
    code = models.ForeignKey(Code, related_name='event_code', on_delete=models.CASCADE, blank=True, null=True,
                             default=None)
    license = models.ForeignKey(License, related_name='event_license', on_delete=models.CASCADE, blank=True, null=True,
                                default=None)

    # colorfield pip install django colorfield

    brand_color_1 = ColorField(default='#6F2EFF')
    brand_color_2 = ColorField(default='#6F2EFF')
    brand_color_3 = ColorField(default='#6F2EFF')

    def _get_unique_slug(self):
        slug_string = self.name
        slug = slugify(slug_string)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event_User(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event.name + '---' + self.user.username)


# class Landing(models.Model):	
# 		client = models.ForeignKey(Event, related_name='landing_event',on_delete=models.CASCADE, blank=True, null=True)#default=1)
# def __str__(self):
# 	return self.name

class LivePlayer(models.Model):
    event = models.ForeignKey(Event, related_name='liveplayer_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    typess = (
        (1, "Live"),
        (2, "SimulatedLive"),
        (3, "VideoPlaceholder"),
    )

    type_video = models.PositiveSmallIntegerField(choices=typess, default=1)
    live_video = models.TextField(blank=True, null=True)
    simulated_live = models.TextField(blank=True, null=True)
    simulated_live_start = models.DateTimeField(default=now)
    simulated_live_ends = models.DateTimeField(default=now)
    placeholder_video = models.TextField(blank=True, null=True)
    use_live_video = models.BooleanField(default=False)
    use_simulated_live = models.BooleanField(default=False)
    use_placeholder_video = models.BooleanField(default=False)
    thumbnail = models.FileField(upload_to='pictures/', blank=True, null=True)

    # si necesitas pasar el valor de type_video a los templates usar {instanciaLivePlayer.type_value}
    def type_value(self):
        return dict(LivePlayer.typess)[self.type_video]

    def __str__(self):
        return str(self.event.name + "-" + str(self.type_value()))


class Chat(models.Model):
    event = models.ForeignKey(Event, related_name='chat_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    embed_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.event.name


class Schedule(models.Model):
    event = models.ForeignKey(Event, related_name='schedule_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.event.name


class Announcement(models.Model):
    event = models.ForeignKey(Event, related_name='announcement_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    name = models.CharField(max_length=149, unique=True)
    # slug = models.SlugField(max_length=149, default='my_name')
    horizontal_banner = models.FileField(upload_to='pictures/', blank=True, null=True)
    horizontal_banner_title = models.CharField(max_length=149, blank=True, null=True)
    horizontal_banner_link = models.URLField(max_length=200, default='https://google.com', blank=True, null=True)
    vertical_banner = models.FileField(upload_to='pictures/', blank=True, null=True)
    vertical_banner_title = models.CharField(max_length=149, blank=True, null=True)
    vertical_banner_link = models.URLField(max_length=200, default='https://google.com', blank=True, null=True)
    link_1 = models.URLField(max_length=200, default='https://google.com')
    link_title_1 = models.CharField(max_length=149, blank=True, null=True)
    link_2 = models.URLField(max_length=200, default='https://google.com', blank=True, null=True)
    link_title_2 = models.CharField(max_length=149, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # def _get_unique_slug(self):
    # 	slug_string = self.name
    # 	slug = slugify(slug_string)
    # 	unique_slug = slug
    # 	num = 1
    # 	while Category.objects.filter(slug=unique_slug).exists():
    # 		unique_slug = '{}-{}'.format(slug, num)
    # 		num += 1
    # 	return unique_slug

    # def save(self, *args, **kwargs):
    # 	if not self.slug:
    # 		self.slug = self._get_unique_slug()
    # 	super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class Resource(models.Model):
    event = models.ForeignKey(Event, related_name='resource_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    title = models.CharField(max_length=149, unique=True)
    link = models.URLField(max_length=200, default='https://google.com', blank=True, null=True)
    thumbnail = models.FileField(upload_to='pictures/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Room(models.Model):
    event = models.ForeignKey(Event, related_name='room_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    name = models.CharField(max_length=149, unique=True)
    slug = models.SlugField(max_length=149, default=None)
    thumbnail = models.FileField(upload_to='pictures/', blank=True, null=True)
    banner = models.FileField(upload_to='pictures/', blank=True, null=True)
    icon = models.CharField(max_length=149, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    own_chat = models.BooleanField(default=False)
    own_liveplayer = models.BooleanField(default=False)
    chat = models.TextField(blank=True, null=True)
    live_video = models.TextField(blank=True, null=True)
    simulated_live = models.TextField(blank=True, null=True)
    simulated_live_start = models.DateTimeField(default=now)
    simulated_live_ends = models.DateTimeField(default=now)
    placeholder_video = models.TextField(blank=True, null=True)
    use_live_video = models.BooleanField(default=False)
    use_simulated_live = models.BooleanField(default=False)
    use_placeholder_video = models.BooleanField(default=False)

    def _get_unique_slug(self):
        slug_string = self.name
        slug = slugify(slug_string)
        unique_slug = slug
        num = 1
        while Room.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Speaker(models.Model):
    event = models.ForeignKey(Event, related_name='speaker_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    name = models.CharField(max_length=149, unique=True)
    slug = models.SlugField(max_length=149, default=None)
    text = models.TextField(blank=True, null=True)
    thumbnail = models.FileField(upload_to='pictures/', blank=True, null=True)

    def _get_unique_slug(self):
        slug_string = self.name
        slug = slugify(slug_string)
        unique_slug = slug
        num = 1
        while Speaker.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Video(models.Model):
    event = models.ForeignKey(Event, related_name='video_event', on_delete=models.CASCADE, blank=True,
                              null=True)  # default=1)
    title = models.CharField(max_length=149, unique=True)
    speaker = models.ForeignKey(Speaker, related_name='video_speaker', on_delete=models.CASCADE, blank=True,
                                null=True)  # default=1)
    room = models.ForeignKey(Room, related_name='video_room', on_delete=models.CASCADE, blank=True,
                             null=True)  # default=1)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)  # date += datetime.timedelta(days=1)
    video = models.TextField(blank=True, null=True)
    resource = models.ForeignKey(Resource, related_name='video_resource', on_delete=models.CASCADE, blank=True,
                                 null=True)  # default=1)
    thumbnail = models.FileField(upload_to='pictures/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


from django.db import models
from ckeditor.fields import RichTextField


# hay que pinches refactorizar las notas por que ya habra ams eventos TTnTT
class Note(models.Model):
    title = models.CharField(max_length=149)
    # slug = models.SlugField(max_length=149, default='my_title')
    text = RichTextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title
    class Meta:
        unique_together = ('title', 'user')

    # text = models.TextField(blank=True, null=True)

    # def _get_unique_slug(self):
    # 	slug_string = self.title
    # 	slug = slugify(slug_string)
    # 	unique_slug = slug
    # 	num = 1
    # 	while Category.objects.filter(slug=unique_slug).exists():
    # 		unique_slug = '{}-{}'.format(slug, num)
    # 		num += 1
    # 	return unique_slug

    # def save(self, *args, **kwargs):
    # 	if not self.slug:
    # 		self.slug = self._get_unique_slug()
    # 	super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# from django.db import models
# from ckeditor.fields import RichTextField

# class Post(models.Model):
#     content = RichTextField()


class Programme(models.Model):
    title = models.CharField(max_length=149, unique=True)
    event = models.ForeignKey(Event, related_name='program_event', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class ProgrammeElement(models.Model):
    title = models.CharField(max_length=149)
    date = models.CharField(max_length=149)
    time = models.TextField(max_length=249)
    room = models.ForeignKey(Room, related_name='programme_element_room', on_delete=models.CASCADE, blank=True, null=True)
    programme = models.ForeignKey(Programme, related_name='programme_element_programme', on_delete=models.CASCADE, blank=True, null=True)
    place_in_programme = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Teamedition(models.Model):
    title = models.CharField(max_length=149)
    content = RichTextField(default="")
    image = models.FileField(upload_to='te/', blank=True, null=True)#,help_text='sube tu pago aqui (pdf o imagen)',)

    def __str__(self):
        return self.title



class Sponsor(models.Model):
    title = models.CharField(max_length=149)
    description = models.TextField(blank=True, null=True) 
    banner_1 = models.FileField(upload_to='banners/', blank=True, null=True)
    use_banner_1 = models.BooleanField(default=False)
    banner_2 = models.FileField(upload_to='banners/', blank=True, null=True)
    use_banner_2 = models.BooleanField(default=False)
    link_1 = models.URLField(default="",null=True, blank=True) 
    link_1_text = models.CharField(max_length=300,blank=True,null=True)
    use_link_1 = models.BooleanField(default=False)
    link_2 = models.URLField(default="",null=True, blank=True) 
    link_2_text = models.CharField(max_length=300,blank=True,null=True)
    use_link_2 = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class SpiritualSupportRequest(models.Model):
    name = models.CharField(max_length=149, unique=True)
    description = RichTextField(default="")
    image = models.FileField(upload_to='spiritualsupport/', blank=True, null=True)

class UserGuideArticle(models.Model):
    # language = models.ForeignKey(Language, related_name='Language_user_guide_article', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=250, verbose_name=u'Title')
    content = RichTextField(default="")
    def __str__(self):
        return self.title