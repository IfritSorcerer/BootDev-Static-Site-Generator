import re
from textnode import TextNode, TextType

img_re = r"!\[(.*?)\]\((.*?)\)"
link_re = r"\s\[(.*?)\]\((.*?)\)"

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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_images(text):
    img_list = re.findall(img_re, text)
    return img_list

def extract_markdown_links(text):
    link_list = re.findall(link_re, text)
    return link_list

def split_nodes_image(old_nodes):  
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        node_images = extract_markdown_images(node.text)
        for image in node_images:
            splitter = f"![{image[0]}]({image[1]})"
            split_text = text.split(splitter, 1)
            if len(split_text) == 2:
                text = split_text[1]
            else:
                text = ""
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMG, image[1]))
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        node_links = extract_markdown_links(text)
        for link in node_links:
            splitter = f"[{link[0]}]({link[1]})"
            split_text = text.split(splitter, 1)
            if len(split_text) == 2:
                text = split_text[1]
            else:
                text = ""
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes