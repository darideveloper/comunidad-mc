-- actions flags: l.user, l.action_time and l.obj_repr

SELECT logs.id, logs.object_repr, users.username, action_flag
FROM public.django_admin_log as logs
left join public.auth_user as users on logs.user_id = users.id
ORDER BY logs.id DESC 