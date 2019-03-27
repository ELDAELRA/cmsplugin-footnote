# coding: utf-8

from django.utils import translation
from cms.plugin_base import CMSPlugin
from djangocms_text_ckeditor.models import Text
from djangocms_text_ckeditor.utils import plugin_tags_to_id_list
from .models import Footnote


def footnotes_and_text_plugins_queryset(page=None, placeholder_slot=None):
    """ Return base footnotes queryset.
    """
    footnote_and_text_plugins = CMSPlugin.objects.filter(
        plugin_type__in=('FootnotePlugin', 'TextPlugin'),
        language=translation.get_language(),
    ).order_by('-position')

    if page:
        footnote_and_text_plugins.filter(placeholder__page=page)

    if placeholder_slot:
        footnote_and_text_plugins.filter(placeholder__slot=placeholder_slot)

    return footnote_and_text_plugins


def get_footnotes_for_page(request, page=None, placeholder_slot=None):
    """ Gets the Footnote instances for `page`, with the correct order.
    """
    footnotes = list()
    plugins_queryset = footnotes_and_text_plugins_queryset(page=page, placeholder_slot=placeholder_slot)

    footnote_dict = Footnote.objects.in_bulk(
        plugins_queryset.filter(plugin_type='FootnotePlugin').values('id')
    )
    text_dict = Text.objects.in_bulk(
        plugins_queryset.filter(plugin_type='TextPlugin').values('id')
    )

    def get_footnote_or_text(plugin_pk, plugin_type):
        """ Return footnote or text object with `plugin_pk` argument from related dict of `plugin_type`.
        """
        if plugin_type == 'FootnotePlugin':
            return footnote_dict.get(plugin_pk, None)
        elif plugin_type == 'TextPlugin':
            return text_dict.get(plugin_pk, None)
        else:
            raise ValueError('The value of `plugin_type` argument must be `FootnotePlugin` or `TextPlugin`')
        return None

    for plugin in plugins_queryset:
        footnote_or_text = get_footnote_or_text(plugin.pk, plugin.plugin_type)
        if footnote_or_text:
            if plugin.plugin_type == 'FootnotePlugin':
                if plugin.parent and not page:
                    footnotes.append(footnote_or_text)
            else:
                for pk in plugin_tags_to_id_list(footnote_or_text.body):
                    footnote = get_footnote_or_text(pk, 'FootnotePlugin')
                    if footnote is not None:
                        footnotes.append(footnote)
    return footnotes
