from django.contrib import admin

# Register your models here.
from .models import Missionary, Supporter, User, Tag, TagRecord,\
                    SearchHistory, ExternalMedia

# Registering tables into admin/
admin.site.register(User)
admin.site.register(Supporter)
admin.site.register(Missionary)
admin.site.register(Tag)
admin.site.register(TagRecord)
admin.site.register(SearchHistory)
admin.site.register(ExternalMedia)
