from django import template

register = template.Library()

register_mul = template.Library()

@register.filter
def get_comment_by_id(comments, comment_id):
    for comment in comments:
        if comment.id == comment_id:
            return comment
    return None




@register_mul.filter
def mul(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''
