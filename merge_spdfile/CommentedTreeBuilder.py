# -*- coding:gbk -*-
from xml.etree import ElementTree

# ElementTree默认不会读取XML中的注释，这里重写构造，以实现缓存xml注释。
class CommentedTreeBuilder(ElementTree.XMLTreeBuilder):

    def __init__(self, html=0, target=None):
        ElementTree.XMLTreeBuilder.__init__(self, html, target)
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ElementTree.Comment, {})
        self._target.data(data)
        self._target.end(ElementTree.Comment)
