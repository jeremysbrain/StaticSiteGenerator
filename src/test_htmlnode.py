import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_node = HTMLNode("a", "val", "", {"href":"google.com", "target": "_blank"})
        #print(HTMLNode("a", "val"))
        #print(test_node)
        print(test_node.props_to_html)
        
        #node = TextNode("This is a text node", TextType.BOLD)
        #node2 = TextNode("This is a text node", TextType.BOLD)
        #self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()