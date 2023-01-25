from . import models 
from django.contrib import admin

# Filter classes
class FilterWeeklyDailyPoints (admin.SimpleListFilter):
    """ Filter points by user name """
    
    # Visible texts
    title = 'Usuario con puntos'
    parameter_name = 'usuario'

    def lookups(self, request, model_admin):
        """ return options """
        
        # Generate options based in available users
        options = []
        for point in model_admin.model.objects.all():
            options.append((point.general_point.user.id, point.general_point.user.user_name))
       
        return tuple(set(options))
    
    def queryset(self, request, queryset):
        """ returns the filtered queryset """
        
        # Return all values
        if self.value() is None:
            return queryset
        
        # Get point who match with the user
        user_id = self.value()
        general_points = models.GeneralPoint.objects.filter(user_id=user_id)
        points_user = queryset.filter (general_point__in=general_points)
        
        return points_user
    
# Admin classes
@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
    
    change_form_template = 'admin/change_form_users.html'    
    list_display = ('id', 'user_name', 'is_active', 'is_admin', 'ranking', 'first_name', 'last_name', 'email', 'phone',)
    list_filter = ('country', 'time_zone', 'is_active', 'is_admin', 'ranking',)
    ordering = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone', 'ranking',)
    search_fields = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone', 'country', 'time_zone')
    search_help_text = "Buscar usuarios por nombre, apellido, email, país o zona horaria"

@admin.register (models.Country)
class AdminCountry (admin.ModelAdmin):
    
    list_display = ('id', 'country')
    ordering = ('id', 'country')
    search_fields = ('country', )
    
@admin.register (models.TimeZone)
class AdminTimeZone (admin.ModelAdmin):
    
    list_display = ('id', 'time_zone')
    ordering = ('id', 'time_zone')
    search_fields = ('time_zone', )
    
@admin.register (models.Stream)
class AdminStream (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'datetime')
    ordering = ('id', 'user', 'datetime')
    list_filter = ('user', 'datetime')
    search_fields = ('user', )
    
@admin.register (models.Comment)
class AdminComment (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'comment', 'datetime', 'status')
    ordering = ('id', 'user', 'stream', 'datetime', 'datetime', 'status')
    list_filter = ('user', 'datetime', 'status')
    search_fields = ('user', 'stream', 'comment')
    
@admin.register (models.WhatchCheck)
class AdminWhatchCheck (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'datetime', 'status')
    ordering = ('id', 'user', 'stream', 'datetime', 'status')
    list_filter = ('user', 'datetime', 'status')
    search_fields = ('user', 'stream')
    
@admin.register (models.Status)
class AdminStatus (admin.ModelAdmin):
    
    list_display = ('id', 'name')
    ordering = ('id', 'name')
    search_fields = ('name',)
    
@admin.register (models.GeneralPoint)
class AdminGeneralPoint (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'datetime')
    ordering = ('id', 'user', 'stream', 'datetime')
    list_filter = ('user', 'stream', 'datetime')
    search_fields = ('user', 'stream')
    
@admin.register (models.WeeklyPoint)
class AdminWeeklyPoint (admin.ModelAdmin):
    
    list_display = ('id', 'general_point')
    ordering = ('id', 'general_point')
    list_filter = (FilterWeeklyDailyPoints,)
    search_fields = ('general_point',)
    
@admin.register (models.DailyPoint)
class AdminDailyPoint (admin.ModelAdmin):
    
    list_display = ('id', 'general_point')
    ordering = ('id', 'general_point')
    list_filter = (FilterWeeklyDailyPoints,)
    search_fields = ('general_point',)
    
@admin.register (models.Ranking)
class AdminRanking (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'points')
    ordering = ('id', 'name', 'points')
    search_fields = ('name',)
    
@admin.register (models.PointsHistory)
class AdminPointsHistory (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'general_points', 'week_points')
    ordering = ('id', 'user', 'general_points', 'week_points')
    search_fields = ('user',)
    
@admin.register (models.Bits)
class AdminBits (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount')
    ordering = ('id', 'user', 'amount')
    list_filter = ('user',)
    search_fields = ('user',)
    
@admin.register (models.TopDailyPoint)
class AdminTopDailyPoint (admin.ModelAdmin):
    
    list_display = ('position', 'user', 'datetime')
    ordering = ('position', 'user', 'datetime')
    list_filter = ('user', 'datetime')
    search_fields = ('user',)