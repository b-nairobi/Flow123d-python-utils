# encoding: utf-8
# author:   Jan Hybs


'''
MdLatex Extension for Python-Markdown
======================================

Converts [[type_value]] to relative links.
'''

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import re
from ist.globals import Globals


def build_url(label, base, end):
    """ Build a url from the label, a base, and an end. """
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', label)
    return '%s%s%s' % (base, clean_label, end)


class MdLinkExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.md = None
        self.config = {
        }

        super(MdLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        # WIKILINK_RE = r'\[\[([\w0-9_ -]+)\]\]'
        WIKILINK_RE = r'\[\[([\w0-9_#-]+)\]\]'
        wikilinkPattern = MdLinks(WIKILINK_RE, { })
        wikilinkPattern.md = md
        md.inlinePatterns.add('mdlinks', wikilinkPattern, "<not_strong")


class MdLinks(Pattern):
    def __init__(self, pattern, config):
        super(MdLinks, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        if m.group(2).strip():
            label = m.group(2).strip()
            element = self.build_element('auto', label)
            return element
        else:
            return ''

    def build_element(self, t, label):
        if t.lower() == 'attribute':
            p = etree.Element('p')
            p.text = 'attribute value here'
            return p

        if t.lower() in ('record', 'abstractrecord', 'selection', 'r', 'a', 's', 'ar', 'auto'):

            # find item which is desired
            result = Globals.get_url_by_name(label)
            item = result[0]
            item_field = result[1]
            a = etree.Element('a')

            if item_field:
                a.text = item_field.href_name
                a.set('href', '#{item_field.href_id}'.format(item_field=item_field))

            elif item:
                a.text = item.href_name
                a.set('href', '#{item.href_id}'.format(item=item))

            return a

        print 'unknown type'
        return None


class StrikeThroughExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.md = None
        self.config = {
        }

        super(StrikeThroughExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        # WIKILINK_RE = r'\[\[([\w0-9_ -]+)\]\]'
        WIKILINK_RE = r'~~([\w0-9_#-]+)~~'
        wikilinkPattern = StrikeThroughPattern(WIKILINK_RE, { })
        wikilinkPattern.md = md
        md.inlinePatterns.add('mdstrikethrough', wikilinkPattern, "<not_strong")


class StrikeThroughPattern(Pattern):
    def __init__(self, pattern, config):
        super(StrikeThroughPattern, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        label = m.group(2).strip()
        if label:
            span = etree.Element('del')
            span.text = label
            return span
        return ''

def makeExtension(*args, **kwargs):
    return StrikeThroughExtension(*args, **kwargs)