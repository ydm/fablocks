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
        nodes = self.parse(block)
        nodes.extend(self.childnodes(block))
        return nodes.render(context)

    def render_image(self, context, block):
        images = self.block.image_set.all()
        if images.count() == 0:
            raise ValueError('block has no images')
        return '<img class="{}" alt="" src="{}">'.format(
            block.text, images[0].image.url
        )

    def render_container(self, context, block):
        return '''\
        <div class="container {}">
          {}
          {}
        </div>'''.format(
            block.text,
            self.parse(block).render(context),
            self.childnodes(block).render(context),
        )

    def render_row(self, context, block):
        return '''\
        <div class="row {}">
          {}
        </div>'''.format(
            block.text,
            self.childnodes(block).render(context)
        )

    def render_col(self, context, block):
        return '''\
        <div class="col-md-4">
          {}
        </div>'''.format(
            self.parse(block).render(context),
        )

    def parse(self, block):
        lexer = template.Lexer(block.text, template.StringOrigin(block.text))
        return template.Parser(lexer.tokenize()).parse()

    def childnodes(self, block):
        return template.NodeList([Node(b) for b in block.children.all()])


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
