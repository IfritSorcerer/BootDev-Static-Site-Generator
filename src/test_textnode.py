import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url(self):
        node = TextNode("this text is a hyperlink", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("this text is a hyperlink", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_no_url(self):
        node = TextNode("this text contains no url", TextType.ITALIC)
        node2 = TextNode("this text contains no url", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode ("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    #===========text_to_html_node Tests===========
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This node is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This node is bold")    
    

if __name__ == "__main__":
    unittest.main()