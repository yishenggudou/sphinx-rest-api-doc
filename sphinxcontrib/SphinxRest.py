#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
from .RestAPIContext import RestAPIContext
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class rest(nodes.General, nodes.Element):
    pass


def html_visit_rest_node(self, node):
    pass
    #rest_api_root = self.builder.config.rest_api_root
    #node["path"]
    # httpdomain_node = nodes.http(uri=refname, **node.attributes)
    # aspect = node["aspect"]
    # width = node["width"]
    # height = node["height"]
    # node.append(httpdomain_node)


def depart_rest_node(self, node):
    pass


class RestDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "desc": directives.unchanged,
        "title": directives.unchanged,
        "summary": directives.unchanged,
        "method": directives.unchanged,
        "example_path": directives.unchanged,
    }
    
    def run(self):
        env = self.state.document.settings.env
        warning = self.state.document.reporter.warning
        config = env.config
        result_node = ViewList()
        def_path = os.path.join(config['rest_api_source_root'], self.arguments[0])
        o = RestAPIContext(
            config['rest_api_domain'],
            def_path
            **self.options
        )
        rst_context = o.get_rst_content()
        print(rst_context)
        node = nodes.section()
        node.document = self.state.document
        with StringIO(rst_context) as fr:
            for index, line in enumerate(fr):
                new_line = line.rstrip()
                print(new_line)
                result_node.append(new_line, "<rest>")
        
        # Parse the rst.
        nested_parse_with_titles(self.state, result_node, node)
        return node.children


def depart_rest_node(self, node):
    pass


_NODE_VISITORS = {
    'html': (html_visit_rest_node, depart_rest_node),
    'latex': (html_visit_rest_node, depart_rest_node),
    # 'latex': (latex_visit_rest, latex_depart_rest),
    # 'man': (unsupported_visit_plantuml, None),  # TODO
    # 'texinfo': (unsupported_visit_plantuml, None),  # TODO
    # 'text': (text_visit_plantuml, None),
}


def setup(app):
    app.setup_extension('sphinxcontrib.httpdomain')
    app.add_node(rest, **_NODE_VISITORS)
    app.add_directive("rest", RestDirective)
    app.add_config_value('rest_api_source_root', '.', '.')
    app.add_config_value('rest_api_domain', 'example.com', 'example.com')
    app.add_config_value('http_request_example_title', 'example.com', 'example.com')
    app.add_config_value('http_request_example_title', 'example.com', 'example.com')
    return {'parallel_read_safe': True}
