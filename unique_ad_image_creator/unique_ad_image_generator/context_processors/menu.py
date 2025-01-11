def menu(request):
    items = {
        'common_items': [
            {'path': 'create_presentation:contacts', 'text': 'Техподдержка'},
            {'path': 'create_presentation:faq', 'text': 'FAQ'},
        ],
    }
    if request.user.is_authenticated:
        items['authenticated_items'] = [
            {
                'path': 'users:password_change',
                'text': 'Изменить пароль',
                'link_light': True
            },
        ]
    if request.user.is_authenticated and request.user.is_superuser:
        items['superuser_items'] = [
            {
                'path': 'image_generator:cabinet',
                'text': 'Кабинет',
                'link_light': True
            },
        ]
    else:
        items['guest_items'] = [
            {'path': 'users:login', 'text': 'Войти'},
        ]
    return items
