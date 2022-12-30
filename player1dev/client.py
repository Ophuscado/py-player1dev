"""
Simple framework for building (web) apps with Python and Flet. The client is made to operate locally, but can be deployed to a server. The server is made to operate on a server, but can be deployed locally. What you have to decide is the exposition and scope of both. Giving public access to the `client.py` will have serious security risks.

It relies on Flet (Flutter) and FastAPI. Flet is a Python library that allows you to build Flutter apps with Python. FastAPI is a Python library that allows you to build web apps with Python.
"""

import importlib

import flet as ft


def main(page: ft.Page, sidebar, navbar):
    page.window_height = 720
    page.window_width = 1280
    page.window_min_height = 600
    page.window_min_width = 800

    def route_change(route):
        page_route = (
            page.route[1:].split("/")[0]
            if page.route.startswith("/") and len(page.route) > 1
            else "home"
        )

        try:
            view = importlib.import_module(f"views.{page_route}")
        except ModuleNotFoundError:
            view = importlib.import_module(f"views.error404")
        page.views.clear()
        page.views.append(
            ft.View(
                f"/{page_route}",
                [view.main(page)],
                appbar=navbar.main(page),
                horizontal_alignment="center",
                vertical_alignment="center",
            )
        )

        page.title = f"Intraneto.com - {page.route}"
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    rail = sidebar.main(page)
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [view for view in page.views],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


ft.app(target=main, view=ft.WEB_BROWSER, route_url_strategy="path")
