from django import template

register = template.Library()


@register.filter
def split(splitable, split_at):
    # split with max limit
    if len(split_at.split("||||")) == 2:
        return splitable.split(split_at.split("||||")[0], int(split_at.split("||||")[1]))

    # normal split without max limitation
    return splitable.split(split_at)