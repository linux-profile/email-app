# coding=utf-8

"""
Utils
"""

__all__ = ['get_field_list']


def get_field_list(model):
    field_list = []
    fields = model._meta.local_fields
    for item in fields:
        if item.is_relation:
            field_list.append(item.name + '_id')
        else:
            field_list.append(item.name)

    return field_list
