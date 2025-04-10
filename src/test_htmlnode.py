import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_node = HTMLNode("a", "val", "", {"href":"google.com", "target": "_blank"})
        self.assertEqual(test_node.props_to_html(), ' href="google.com" target="_blank"')
        #print(HTMLNode("a", "val"))
        #print(test_node)
        #print(test_node.props_to_html)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
        #node = TextNode("This is a text node", TextType.BOLD)
        #node2 = TextNode("This is a text node", TextType.BOLD)
        #self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()