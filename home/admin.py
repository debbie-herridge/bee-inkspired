from django.contrib import admin

from .models import * 


admin.site.register(Tag)
admin.site.register(Design)
admin.site.register(Booking)
admin.site.register(Enquiry)
admin.site.register(Review)