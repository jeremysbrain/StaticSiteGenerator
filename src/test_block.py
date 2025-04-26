import unittest

from block import *



class TestBlock(unittest.TestCase):
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_html_node(self):
        markdown = """# Main Heading

This is a paragraph.

* First item
* Second item

1. Numbered item one
2. Numbered item two

> This is a quote

```code
print("Hello world")
```"""
        
        node = markdown_to_html_node(markdown)
        
        # Test the root node is a div
        assert node.tag == "div"
        # Test we have 6 child blocks
        assert len(node.children) == 6
        
        # Test each block type
        assert node.children[0].tag == "h1"
        assert node.children[0].children[0].value == "Main Heading"
        
        assert node.children[1].tag == "p"
        assert node.children[1].children[0].value == "This is a paragraph."
        
        # Test unordered list
        assert node.children[2].tag == "ul"
        assert len(node.children[2].children) == 2  # two list items
        
        # Test ordered list
        assert node.children[3].tag == "ol"
        assert len(node.children[3].children) == 2  # two list items
        
        # Test quote
        assert node.children[4].tag == "blockquote"
        
        # Test code block
        assert node.children[5].tag == "pre"
        assert node.children[5].children[0].tag == "code"

if __name__ == "__main__":
    unittest.main()