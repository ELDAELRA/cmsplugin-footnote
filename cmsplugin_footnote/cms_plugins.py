# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from cms.plugin_pool import plugin_pool
from .models import Footnote
from .utils import get_footnotes_for_page


class FootnotePlugin(TextPlugin):
    model = Footnote
    name = _('Footnote')
    render_template = 'cmsplugin_footnote/footnote_symbol.html'
    text_enabled = True
    admin_preview = False

    def render(self, context, instance, placeholder_slot):
        context = super(FootnotePlugin, self).render(context, instance, placeholder_slot)
        request = context['request']
        footnotes = get_footnotes_for_page(request, page=request.current_page, placeholder_slot=placeholder_slot)
        if instance in footnotes:
            context["counter"] = footnotes.index(instance) + 1
        return context


plugin_pool.register_plugin(FootnotePlugin)
