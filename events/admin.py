from django.contrib import admin
from events.models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources



# admin.site.register(Client)
# admin.site.register(Event) 
@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
	pass
admin.site.register(LivePlayer)
admin.site.register(Chat)
# admin.site.register(Schedule)
# admin.site.register(Announcement)
# @admin.register(Announcement)
class AnnouncementAdmin(ImportExportModelAdmin):
	pass
admin.site.register(Resource)
# admin.site.register(Room)
@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
	pass
admin.site.register(Video)
# admin.site.register(Speaker)
@admin.register(Speaker)
class SpeakerAdmin(ImportExportModelAdmin):
	pass
# admin.site.register(Note)
@admin.register(Note)
class NoteAdmin(ImportExportModelAdmin):
	pass
# admin.site.register(Event_User)
@admin.register(Event_User)
class Event_UserAdmin(ImportExportModelAdmin):
	pass

@admin.register(ProgrammeElement)
class ProgramElementAdmin(ImportExportModelAdmin):
	pass

@admin.register(Programme)
class ProgramAdmin(ImportExportModelAdmin):
	pass

@admin.register(Teamedition)
class TeameditionAdmin(ImportExportModelAdmin):
	pass

@admin.register(Sponsor)
class SponsorAdmin(ImportExportModelAdmin):
	pass
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		form.base_fields["link_1"].label = "Link 1 (https://www.google.com):"
		return form

@admin.register(SpiritualSupportRequest)
class SpiritualSupportRequestAdmin(ImportExportModelAdmin):
	list_display = ['name', 'description', ]

@admin.register(UserGuideArticle)
class UserGuideArticleAdmin(ImportExportModelAdmin):
	pass

