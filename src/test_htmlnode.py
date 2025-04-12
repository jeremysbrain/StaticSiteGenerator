import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()