import re

from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "_"
    CODE = "`"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, TextNode):
        return (self.text_type == TextNode.text_type) and (self.text == TextNode.text) and (self.url == TextNode.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def find_first_pair(text, delimiter):

    start = text.find(delimiter)

    if start == -1:
        return None
    
    end = text.find(delimiter, start + len(delimiter))

    if end == -1:
        raise Exception ("No closing delimiter found")
    
    return start, end

def split_delim(text, delimiter, text_type):
    current_nodes = []

    try:
        first_delim, second_delim = find_first_pair(text, delimiter)
    except Exception:
        current_nodes.append(TextNode(text,TextType.TEXT))
        return current_nodes

    before_text = text[0:first_delim]
    if before_text:
        current_nodes.append(TextNode(before_text,TextType.TEXT))
    
    between_text = text[first_delim+len(delimiter):second_delim]
    if between_text.strip():
        current_nodes.append(TextNode(between_text, text_type))

    after_text = text[second_delim+len(delimiter):len(text)]

    if after_text.strip():
        current_nodes.extend(split_delim(after_text, delimiter, text_type))
        
    return current_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    #return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

#def split_nodes_image(old_nodes):
#    current_nodes = []
#    for n in old_nodes:
#        current_nodes.extend(split_images(n.text, n.text_type))
#    return current_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_images(text,text_type):
    current_nodes = []
    images_extracted = extract_markdown_images(text)
    image_count = len(images_extracted)

    if not text:
        return current_nodes

    if image_count < 1:
        current_nodes.append(TextNode(text,text_type))
        return current_nodes
    
    markdown_image_to_split = f"![{images_extracted[0][0]}]({images_extracted[0][1]})"
    split_text = text.split(markdown_image_to_split)

    if split_text[0]:
        current_nodes.append(TextNode(split_text[0],text_type))

    current_nodes.append(TextNode(images_extracted[0][0],TextType.IMAGE,images_extracted[0][1]))

    if split_text[1]:
        current_nodes.extend(split_images(split_text[1],text_type))

    return current_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

#def split_nodes_link(old_nodes):
#    current_nodes = []
#    for n in old_nodes:
#        current_nodes.extend(split_links(n.text,n.text_type))
#    return current_nodes

def split_links(text,text_type):
    current_nodes = []
    links_extracted = extract_markdown_links(text)
    link_count = len(links_extracted)

    if not text:
        return current_nodes

    if link_count < 1:
        current_nodes.append(TextNode(text,text_type))
        return current_nodes
    
    markdown_link_to_split = f"[{links_extracted[0][0]}]({links_extracted[0][1]})"
    split_text = text.split(markdown_link_to_split)

    if split_text[0]:
        current_nodes.append(TextNode(split_text[0],text_type))

    current_nodes.append(TextNode(links_extracted[0][0],TextType.LINK,links_extracted[0][1]))

    if split_text[1]:
        current_nodes.extend(split_links(split_text[1],text_type))

    return current_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list
