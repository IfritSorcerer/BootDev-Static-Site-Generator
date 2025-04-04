import unittest
from textnode import TextNode, TextType
from text_to_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextToMarkdown(unittest.TestCase):
    #===========split_node_delimiter Tests===========
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
    
    #===========extract_markdown_images/extract_markdown_links Test===========
        def test_extract_markdown_images(self):
            matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ")])

        def test_extract_markdown_links(self):
            matches = extract_markdown_links(
                "This is a text with a [link](https://www.boot.dev)"
            )
            self.assertListEqual([("link", "https://www.boot.dev")])

        
        def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


        def test_split_links(self):
            node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
                TextType.TEXT
            )
            new_nodes = split_nodes_link([node])
            self.assertEqual(
            [
                TextNode("This is text with a link" , TextType.TEXT), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode( "and" , TextType.TEXT), 
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
                ],
                new_nodes    
            )


        def test_text_to_textnodes(self):
            node = TextNode(
                "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            )
            new_nodes = text_to_textnodes(node.text)
            self.assertEqual(
                [
                    TextNode("This is" , TextType.TEXT), 
                    TextNode("text", TextType.TEXT), 
                    TextNode( "with an" , TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode("word and a" , TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode( "and an" , TextType.TEXT), 
                    TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a" , TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev")
                ],
                new_nodes
            )

    if __name__ == "main":
        unittest.main()