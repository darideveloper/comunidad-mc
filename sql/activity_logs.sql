-- actions flags: 1:'Add',2:'Change',3:'Delete'

SELECT logs.id, logs.object_repr, users.username, action_flag
FROM public.django_admin_log as logs
left join public.auth_user as users on logs.user_id = users.id
ORDER BY logs.id DESC 