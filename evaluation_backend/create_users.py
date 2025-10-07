# 执行方法：python manage.py shell < create_users.py

from django.contrib.auth.models import User

# 创建超级用户
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Created superuser: admin')

# 创建普通用户
if not User.objects.filter(username='user').exists():
    user = User.objects.create_user('user', 'user@example.com', 'user123')
    user.save()
    print('Created user: user')

print('User setup complete!')