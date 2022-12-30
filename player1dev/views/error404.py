import os

import flet as ft


def main(page: ft.Page):
    return ft.Column(
        [
            ft.Markdown(
                open(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "content",
                        "error404.md",
                    )
                ).read()
            ),
        ],
        expand=1,
        width=800,
        alignment="center",
    )
