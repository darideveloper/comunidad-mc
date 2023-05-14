from django.contrib import admin

# @admin.register (models.Donation)
# class AdminDonation (admin.ModelAdmin):
    
#     list_display = ('id', 'user', 'stream', 'minute', 'amount', 'message', 'status')
#     list_filter = ('status', 'user')
#     ordering = ('-id', 'user', 'stream', 'minute', 'amount', 'message', 'status')
#     search_fields = ('user', 'stream', 'message')
#     list_per_page = 20
#     raw_id_fields = ('stream',)
    
#     def get_queryset(self, request):
        
#         # Get admin type
#         user_auth = request.user
#         admin_type = tools.get_admin_type(user_auth=user_auth)

#         if admin_type == "admin platino":
#             # Get all users of the current admin
#             users = app_models.User.objects.filter(user_auth=user_auth)
            
#             # Render only streams of the current user
#             return models.Donation.objects.filter(stream__user__in=users)
            
#         # Render all streams
#         return models.Donation.objects.all()   
