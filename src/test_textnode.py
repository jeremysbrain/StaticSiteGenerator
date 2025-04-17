import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        self.assertEqual(TextNode("This is a text node", TextType.BOLD, "boot.dev"), TextNode("This is a text node", TextType.BOLD, "boot.dev"))
        self.assertNotEqual(TextNode("this is a text node", TextType.BOLD, "boot.dev"), TextNode("This is a text node", TextType.BOLD, "boot.dev"))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
            text_node = [TextNode("This is text with a `code block` word", TextType.TEXT)]
            self.assertEqual(split_nodes_delimiter(text_node,"`",TextType.CODE), [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ])
            
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))
    
    def test_extract_markdown_links(self):
         self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))
         

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
         node = TextNode(
              "This is a link [link](https://google.com) and [another link](https://bing.com)",
              TextType.TEXT
         )
         new_nodes = split_nodes_link([node])
         self.assertListEqual(
              [
                   TextNode("This is a link ",TextType.TEXT),
                   TextNode("link", TextType.LINK, "https://google.com"),
                   TextNode(" and ", TextType.TEXT),
                   TextNode("another link", TextType.LINK, "https://bing.com"),
              ],
              new_nodes,
         )


if __name__ == "__main__":
    unittest.main()