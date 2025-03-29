class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props 

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False    
        return ( self.tag == other.tag and 
                 self.value == other.value and 
                 self.children == other.children and
                 self.props == other.props          
        )

    def to_html(self):
        raise NotImplementedError("Remember to implement")

    def props_to_html(self, props):
        if not props:
            return ""
        prop_html = ""
        for item in props:
            prop_html += f" {item}='{props[item]}'"
        return prop_html

    
class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if value is None:
            raise ValueError("LeafNode requires a value!")
        super().__init__(tag, value, [], props)   
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value!")

        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html(self.props)}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props = None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node requires a tag!")

        if self.children is None:
            raise ValueError("Parent Node requires a value!")

        leaf_list = []

        for item in self.children:
            leaf_list.append(item.to_html())

        return f"<{self.tag}{self.props_to_html(self.props)}>{"".join(leaf_list)}</{self.tag}>"