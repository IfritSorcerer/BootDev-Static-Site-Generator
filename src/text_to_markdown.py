from textnode import TextNode, TextType

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


