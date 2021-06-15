import json
import notion
import os
from notion.client import NotionClient
from notion2md.color import *
from notion2md.exporter import create_dir, PageBlockExporter
from pathlib import Path
from tqdm import tqdm


# export the markdown file(string).
output_folder = Path('./notion2md_output')


def export_cli(token_v2=None, url=None, bmode=-1):
    create_dir(output_folder)

    if token_v2 is None:
        client = parse_token()
    else:
        client = NotionClient(token_v2=token_v2)
    if url is None:
        url = input("Enter Notion Page Url: ")
    if bmode == -1:
        inp = input("Will you export the Notion Page as blog post? [y/n]")
        if inp == "y":
            blog_mode = True
        elif inp == "n":
            blog_mode = False
        else:
            print("Invaild Input -> Set None")
    else:
        blog_mode = bool(bmode)

    exporter = PageBlockExporter(url, client, blog_mode=blog_mode)
    exporter.create_main_folder(output_folder)
    exporter.create_image_foler()
    exporter.create_file()
    if '_collection' in vars(exporter.page):
        export_db(exporter, client, blog_mode)
    else:
        export(exporter)

    print("\nExporter successfully exported notion page to markdown")


def parse_token():
    """ Get 'token_v2' from the json file.

    - Save the token in the json if use the Exporter first time.
    - Parse the token in the json if entered the token before.
    < Never Share your token_v2 with others >\n
    Returns:
        client(NotionClient): return notion client object.
    """
    Error = False
    try:
        with open(output_folder / "notion_token.json", 'r') as json_read:
            data = json.load(json_read)
        token = data["token"]
    except:
        token = None
    while True:
        if token is None or Error:
            token = input("Enter Token_v2: ")
        try:
            client = NotionClient(token_v2=token)
            notion_token = {}
            notion_token["token"] = token
            with open(output_folder / "notion_token.json", 'w') as json_make:
                json.dump(notion_token, json_make, indent=4)
            return client
        except:
            print("[Error] Invaild Token_v2. Enter Token_v2 again")
            Error = True


def export(exporter):
    """ Recursively export page block with its sub pages

    Args:
        exporter(PageBlockExporter()): export page block
    """
    exporter.page2md()
    exporter.write_file()
    for sub_exporter in exporter.sub_exporters:
        export(sub_exporter)


def export_db(exporter, client, blog_mode):
    pbar = tqdm(exporter.page.collection.get_rows())
    for collection in pbar:
        ec_url = collection.get_browseable_url()
        ec = PageBlockExporter(ec_url, client, blog_mode=blog_mode)
        pbar.set_description(f"{blue}export {ec.title}{end}")  # set export_db description
        ec.create_main_folder(exporter.dir)
        ec.create_image_foler()
        ec.create_file()
        export(ec)
