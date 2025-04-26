import re
from enum import Enum

from htmlnode import *
from textnode import *

class BlockType(Enum):
    heading = "heading"
    quote = "quote"
    code = "code"
    ordered_list = "ordered_list"
    unordered_list = "unordered list"
    paragraph = "paragraph"

def markdown_to_blocks(markdown):
    md_split = markdown.split("\n\n")
    block_list = []
    for b in md_split:
        if b != "":
            block_list.append(b.strip())
    return block_list

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.paragraph
        return BlockType.quote
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.paragraph
        return BlockType.unordered_list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.paragraph
            i += 1
        return BlockType.ordered_list
    return BlockType.paragraph

def markdown_to_html_node(markdown):
    block_list, block_html = [], []
    block_list.extend(markdown_to_blocks(markdown))
    
    for b in block_list:
        block_type = block_to_block_type(b)

        match (block_type):
            case BlockType.code:
                block_html.append(node_code(b))
            case BlockType.quote:
                block_html.append(node_quote(b))
            case BlockType.heading:
                block_html.append(node_heading(b))
            case BlockType.unordered_list:
                block_html.append(node_ul(b))
            case BlockType.ordered_list:
                block_html.append(node_ol(b))
            case BlockType.paragraph:
                block_html.append(node_paragraph(b))
            case __:
                raise Exception("BlockType not found: ", b)
    return ParentNode("div", block_html)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

# HELPER FUNCTIONS FOR HTML

def node_code(block):
    split_lines = block.split("\n")[1:-1]
    text = "\n".join(split_lines)

    node_code = []
    #node_text.append(LeafNode("text", text))
    node_text = text_to_children(text)
    node_code.append(ParentNode("code", node_text))
    return ParentNode("pre", node_code)

def node_quote(block):
    split_lines = block.split("\n")
    text_list = []
    for l in split_lines:
        text_list.append(l.strip("> "))
    
    text = "\n".join(text_list)
    
    #node_text = []
    #node_text.append(LeafNode("text", text))
    node_text = text_to_children(text)
    return ParentNode("blockquote", node_text)

def node_heading(block):
    text = re.findall(r"^(#{1,6}) ", block)
    if len(text) == 1:
        header_length = len(text[0]) + 1
        node_text = text_to_children(block[header_length:])
        #node_text = []
        #node_text.append(LeafNode("text", block[header_length:]))
        html_tag = "h" + str(header_length - 1)
        return ParentNode(html_tag, node_text)
    else:
        raise Exception("Invalid heading")

def node_ul(block):
    split_lines = block.split("\n")
    list_items = []
    for l in split_lines:
        #if re.search(r"^[\*\-] ", l):
            #node_text = LeafNode("text", l[2:])
        node_text = text_to_children(l[2:])
        list_items.append(ParentNode("li", node_text))
    return ParentNode("ul", list_items)

def node_ol(block):
    split_lines = block.split("\n")
    list_items = []
    for l in split_lines:
        #match = re.findall(r"^((\d+)\.( +)?)?(.*)$", l)
        #node_text = LeafNode("text", match[-1])
        #node_text = text_to_children(match[-1])
        node_text = text_to_children(l[3:])
        list_items.append(ParentNode("li", node_text))
    return ParentNode("ol", list_items)

def node_paragraph(block):
    #node_text = []
    #node_text.append(LeafNode("text", block))
    split_lines = block.split("\n")
    node_text = text_to_children(" ".join(split_lines))
    return ParentNode("p", node_text)