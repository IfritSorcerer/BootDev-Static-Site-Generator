import unittest
from textnode import TextNode, TextType
from text_to_markdown import split_nodes_delimiter

class TestTextToMarkdown(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def no_split_needed(self):
        node = TextNode("This is plain text", TextType.TEXT)
        expected = [node]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is a `broken code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    if __name__ == "main":
        unittest.main()