import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #===========HTMLNode Tests===========
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph tag", None, {"href":"https://www.boot.dev"})
        node2 = HTMLNode("p", "This is a paragraph tag", None, {"href":"https://www.boot.dev"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph tag", None, {"href":"https://www.boot.dev"})
        test_str = node.props_to_html(node.props)
        self.assertTrue(test_str)

    def test_notEqual_url(self):
        node = HTMLNode("h1", "This is a header", None, None)
        node2 = HTMLNode("h1", "This is a header", None, {"href": "https://www.boot.dev"})
        self.assertNotEqual(node, node2) 


    #===========LeafNode Tests===========
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "hello world")
        self.assertEqual(node.to_html(), "<p>hello world</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "click here", {"href":"https://www.boot.dev", "target":"_blank"})
        self.assertEqual(node.to_html(), "<a href='https://www.boot.dev' target='_blank'>click here</a>")


    #===========ParentNode Tests===========
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parentnode(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent_node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_parent_node(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("p", [
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text")
                ])
            ],
        )
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<p><i>italic text</i>Normal text</p></p>")

if __name__ == "__main__":
    unittest.main()