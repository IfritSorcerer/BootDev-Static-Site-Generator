import unittest
from block_markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = ("# This is a heading"+"\n\n"+
                "            This is a paragraph of text. It has some **bold** and "+
                "*italic* words inside of it."+"\n\n"
                "- This is a list item"+"\n"
                "- This is another list item"
        )
        expected = ["# This is a heading",
                "This is a paragraph of text. It has some **bold** and "+
                "*italic* words inside of it.",
                "- This is a list item\n"+
                "- This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(text),expected)
    
    def test_block_to_block_type(self):
        text = "\n".join([
            "- Hello",
            "- This is",
            "- An Unordered List"
        ])
        expected = BlockType.ULIST
        self.assertEqual(block_to_block_type(text), expected)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = "This is a **bolded** paragraph text in a p tag here"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>bolded</b> paragraph text in a p tag here</p></div>")

    def test_paragraphs(self):
        md = """
This is a **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")

    def test_lists(self):
        md = """
- This is a list
- With items
- And _more_ items

1. This is an `ordered list`
2. With items
3. And more items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is a list</li><li>With items</li><li>And <i>more</i> items</li></ul><ol><li>This is an <code>ordered list</code></li><li>With items</li><li>And more items</li></ol></div>")
    
    def test_headings(self):
        md = """
# This is an h1

This is a paragraph text

## This is an h2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is an h1</h1><p>This is a paragraph text</p><h2>This is an h2</h2></div>")
    
    def test_blockquote(self):
        md = """
> This is a 
> Blockquote block

This is a paragraph text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><blockquote>This is a Blockquote block</blockquote><p>This is a paragraph text</p></div>")

if __name__ == "__main__":
    unittest.main()