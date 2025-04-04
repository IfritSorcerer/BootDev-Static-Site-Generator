from textnode import TextNode, TextType
import re

img_re = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
link_re = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_node = node.text.split(delimiter)
            
            if len(split_node) % 2 == 0:
                raise ValueError("Invalid Markdown Syntax: Unmatched Delimiter")
                
            for item, part in enumerate(split_node):
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT if item % 2 == 0 else text_type))

        else:
            new_nodes.append(node)

    return new_nodes

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
        if text !="":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    if True:
        nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)

    if True:
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    if True:
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    if True:
        nodes = split_nodes_image(nodes)

    if True:
        nodes = split_nodes_link(nodes)
    return nodes
