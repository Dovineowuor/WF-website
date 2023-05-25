from django.test import TestCase, SimpleTestCase

from bs4 import BeautifulSoup

from content_migration.management.commands.shared import (
    create_document_link_block,
    create_image_block,
    extract_image_urls,
    fetch_file_bytes,
    parse_body_blocks,
    remove_pullquote_tags,
    create_media_embed_block,
    extract_pullquotes,
)

WESTERN_FRIEND_LOGO = "https://westernfriend.org/sites/default/files/logo-2020-%20transparency-120px_0.png"
WESTERN_FRIEND_LOGO_FILE_NAME = "logo-2020-%20transparency-120px_0.png"


class RemovePullquoteTagsSimpleTestCase(SimpleTestCase):
    def test_remove_pullquote_tags(self) -> None:
        soup_context = BeautifulSoup(
            """<p>Some text[pullquote]with a pullquote[/pullquote]</p>""",
            "html.parser",
        )  # noqa: E501
        input_bs4_tag = soup_context.find("p")
        output_bs4_tag = remove_pullquote_tags(input_bs4_tag)  # type: ignore
        expected_bs4_tag = BeautifulSoup(
            """<p>Some textwith a pullquote</p>""",
            "html.parser",
        ).find("p")

        self.assertEqual(output_bs4_tag, expected_bs4_tag)

    def test_remove_pullquote_tags_with_multiple_pullquotes(self) -> None:
        soup_context = BeautifulSoup(
            """<p>Some text [pullquote]with a pullquote[/pullquote] and another [pullquote]with a pullquote[/pullquote]</p>""",  # noqa: E501
            "html.parser",
        )
        input_bs4_tag = soup_context.find("p")
        output_bs4_tag = remove_pullquote_tags(input_bs4_tag)  # type: ignore
        expected_bs4_tag = BeautifulSoup(
            """<p>Some text with a pullquote and another with a pullquote</p>""",
            "html.parser",
        ).find("p")

        self.assertEqual(output_bs4_tag, expected_bs4_tag)


class ExtractPullquotesSimpleTestCase(SimpleTestCase):
    def test_extract_pullquotes(self) -> None:
        input_html = """<p>Some text[pullquote]with a pullquote[/pullquote]</p>"""
        output_pullquotes = extract_pullquotes(input_html)
        expected_pullquotes = ["with a pullquote"]
        self.assertEqual(output_pullquotes, expected_pullquotes)

    def test_extract_pullquotes_with_multiple_pullquotes(self) -> None:
        input_html = """<p>Some text[pullquote]with a pullquote[/pullquote] and another [pullquote]with a pullquote[/pullquote]</p>"""  # noqa: E501
        output_pullquotes = extract_pullquotes(input_html)
        expected_pullquotes = ["with a pullquote", "with a pullquote"]
        self.assertEqual(output_pullquotes, expected_pullquotes)

    def test_extract_pullquotes_with_none_as_input(self) -> None:
        input_html = None

        with self.assertRaises(TypeError):
            extract_pullquotes(input_html)  # type: ignore


class CreateMediaEmbedBlockTestCase(TestCase):
    def test_create_media_embed_block(self) -> None:
        self.MaxDiff = None
        input_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        output_media_embed_block = create_media_embed_block(input_url)

        self.assertEqual(
            output_media_embed_block[1].url,
            input_url,
        )


class TestExtractImages(SimpleTestCase):
    def test_extract_image_urls(self) -> None:
        input_html = (
            """<p>Some text<img src="https://www.example.com/image.jpg" /></p>"""
        )
        output_images = extract_image_urls(input_html)
        expected_images = ["https://www.example.com/image.jpg"]
        self.assertEqual(output_images, expected_images)


class ParseBodyBlocksTestCase(TestCase):
    def test_parse_body_blocks(self) -> None:
        self.MaxDiff = None
        input_html = """<p>Some text[pullquote]with a pullquote[/pullquote]</p>"""
        output_blocks = parse_body_blocks(input_html)
        expected_blocks = [
            (
                "pullquote",
                "with a pullquote",
            ),
            (
                "rich_text",
                """<p>Some textwith a pullquote</p>""",
            ),
        ]

        self.assertEqual(
            output_blocks,
            expected_blocks,
        )

    def test_parse_body_blocks_witn_none_as_input(self) -> None:
        input_html = ""

        ouptut_blocks = parse_body_blocks(input_html)
        expected_blocks: list = []

        self.assertEqual(
            ouptut_blocks,
            expected_blocks,
        )


class FetchFileBytesTestCase(TestCase):
    def test_fetch_file_bytes(self) -> None:
        self.MaxDiff = None

        output_file_bytes = fetch_file_bytes(WESTERN_FRIEND_LOGO)

        self.assertEqual(
            output_file_bytes.file_name,
            WESTERN_FRIEND_LOGO_FILE_NAME,
        )


class TestCreateDocumentLinkBlock(TestCase):
    def test_create_document_link_block(self) -> None:
        input_url = "https://ia600400.us.archive.org/33/items/friendsbulletinp525unse_2/friendsbulletinp525unse_2.pdf"
        input_file_name = "friendsbulletinp525unse_2.pdf"

        file_bytes = fetch_file_bytes(input_url)

        output_document_link_block = create_document_link_block(
            input_file_name,
            file_bytes.file_bytes,
        )
        output_file_name = output_document_link_block[1].title

        self.assertEqual(
            output_file_name,
            input_file_name,
        )


class CreateImageBlockTestCase(TestCase):
    def test_create_image_block(self) -> None:
        file_bytes = fetch_file_bytes(WESTERN_FRIEND_LOGO)
        output_image_block = create_image_block(
            file_name=file_bytes.file_name,
            file_bytes=file_bytes.file_bytes,
        )
        output_filename_start = output_image_block[1]["image"].filename[:5]
        expected_filename_start = WESTERN_FRIEND_LOGO_FILE_NAME[:5]

        self.assertEqual(
            output_filename_start,
            expected_filename_start,
        )
