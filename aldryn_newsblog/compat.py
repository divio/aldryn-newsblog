def toolbar_edit_mode_active(request):
    try:
        # cms 3.4.5 compat
        return request.toolbar.edit_mode
    except AttributeError:
        return request.toolbar.edit_mode_active
