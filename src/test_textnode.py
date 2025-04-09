import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        self.assertEqual(TextNode("This is a text node", TextType.BOLD, "boot.dev"), TextNode("This is a text node", TextType.BOLD, "boot.dev"))
        self.assertNotEqual(TextNode("this is a text node", TextType.BOLD, "boot.dev"), TextNode("This is a text node", TextType.BOLD, "boot.dev"))

if __name__ == "__main__":
    unittest.main()