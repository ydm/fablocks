# -*- coding: utf-8 -*-

from django import template
from fablocks import models


register = template.Library()


class Node(template.Node):

    def __init__(self, block):
        self.block = block

        # lexer = template.Lexer(block.body, template.StringOrigin(block.body))
        # nodes = template.Parser(lexer.tokenize()).parse()

        # if block.type == 'text':
        #     self.nodelist = template.NodeList(nodes)

    def render(self, context):
        fn = getattr(self, 'render_%s' % self.block.type)
        return fn(context, self.block)

    def render_html(self, context, block):
        nodelist = self.parse(block)
        nodelist.extend([Node(b) for b in block.children.all()])
        return nodelist.render(context)

    def render_image(self, context, block):
        pass

    def parse(self, block):
        lexer = template.Lexer(block.text, template.StringOrigin(block.text))
        return template.Parser(lexer.tokenize()).parse()


@register.tag('fablock')
def do_fablock(parser, token):
    try:
        _, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r requires a single SLUG argument' % token.split_contents()[0]
        )

    block = models.Block.objects.get(slug=slug)
    return Node(block)
