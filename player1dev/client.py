"""
A framework for perfectionists to build at light speed. Powered by Flet (Flutter) and FastAPI.
"""

import importlib
import itertools
import logging
import os
import sys
from re import T

import flet
from flet import (
    AlertDialog,
    AppBar,
    ButtonStyle,
    Card,
    Checkbox,
    Column,
    Container,
    Control,
    Draggable,
    DragTarget,
    ElevatedButton,
    FloatingActionButton,
    GridView,
    Icon,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    TemplateRoute,
    Text,
    TextButton,
    TextField,
    UserControl,
    View,
    alignment,
    border,
    border_radius,
    colors,
    icons,
    margin,
    padding,
    theme,
)
from flet.buttons import RoundedRectangleBorder

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


class DataStore:
    # def add_board(self, model) -> None:
    #     raise NotImplementedError

    # def get_board(self, id) -> "Board":
    #     raise NotImplementedError

    # def get_boards(self) -> list["Board"]:
    #     raise NotImplementedError

    # def update_board(self, model, update):
    #     raise NotImplementedError

    # def remove_board(self, board) -> None:
    #     raise NotImplementedError

    def add_user(self, model) -> None:
        raise NotImplementedError

    def get_users(self) -> list["User"]:
        raise NotImplementedError

    def get_user(self, id) -> "User":
        raise NotImplementedError

    def remove_user(self, id) -> None:
        raise NotImplementedError

    # def add_list(self, board, model) -> None:
    #     raise NotImplementedError

    # def get_lists(self) -> list["BoardList"]:
    #     raise NotImplementedError

    # def get_list(self, id) -> "BoardList":
    #     raise NotImplementedError

    # def get_lists_by_board(self, board) -> list["BoardList"]:
    #     raise NotImplementedError

    # def remove_list(self, board, id) -> None:
    #     raise NotImplementedError

    # def add_item(self, board_list, model) -> None:
    #     raise NotImplementedError

    # def get_items(self, board_list) -> list["Item"]:
    #     raise NotImplementedError

    # def get_item(self, id) -> "Item":
    #     raise NotImplementedError

    # def get_items_by_board(self, board) -> list["Item"]:
    #     raise NotImplementedError

    # def remove_item(self, board_list, id) -> None:
    #     raise NotImplementedError


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password


class Sidebar(UserControl):
    def __init__(self, app_layout, store: DataStore, page):
        super().__init__()
        self.store: DataStore = store
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text(view_name),
                label=view_name,
                icon=icons.VIEW_LIST,
                selected_icon=icons.VIEW_LIST,
            )
            for view_name in [
                module_name.replace(".py", "")
                for module_name in os.listdir("views")
                if module_name.endswith(".py") and module_name != "__init__.py"
            ]
        ]

        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            extended=True,
            height=self.top_nav_items.__len__() * 48,
        )
        self.bottom_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.bottom_nav_change,
            extended=True,
            expand=True,
            bgcolor=colors.BLUE_GREY,
        )
        self.toggle_nav_rail_button = IconButton(icons.ARROW_BACK)

    def build(self):
        self.view = Container(
            content=Column(
                [
                    Row(
                        [
                            Text("Built-in"),
                        ],
                        alignment="spaceBetween",
                    ),
                    # divider
                    Container(
                        bgcolor=colors.BLACK26,
                        border_radius=border_radius.all(30),
                        height=1,
                        alignment=alignment.center_right,
                        width=220,
                    ),
                    self.top_nav_rail,
                    # divider
                    Container(
                        bgcolor=colors.BLACK26,
                        border_radius=border_radius.all(30),
                        height=1,
                        alignment=alignment.center_right,
                        width=220,
                    ),
                    Row(
                        [
                            Text("Plug-in"),
                        ],
                        alignment="spaceBetween",
                    ),
                    # divider
                    Container(
                        bgcolor=colors.BLACK26,
                        border_radius=border_radius.all(30),
                        height=1,
                        alignment=alignment.center_right,
                        width=220,
                    ),
                    self.bottom_nav_rail,
                ],
                tight=True,
            ),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            expand=True,
            bgcolor=colors.BLUE_GREY,
            visible=self.nav_rail_visible,
        )
        return self.view

    def sync_board_destinations(self):
        # boards = self.store.get_boards()
        boards = []
        self.bottom_nav_rail.destinations = []
        for i in range(len(boards)):
            b = boards[i]
            self.bottom_nav_rail.destinations.append(
                NavigationRailDestination(
                    label_content=TextField(
                        value=b.name,
                        hint_text=b.name,
                        text_size=12,
                        read_only=True,
                        on_focus=self.board_name_focus,
                        on_blur=self.board_name_blur,
                        border="none",
                        height=50,
                        width=150,
                        text_align="start",
                        data=i,
                    ),
                    label=b.name,
                    selected_icon=icons.CHEVRON_RIGHT_ROUNDED,
                    icon=icons.CHEVRON_RIGHT_OUTLINED,
                )
            )
        self.view.update()

    def toggle_nav_rail(self, e):
        self.view.visible = not self.view.visible
        self.view.update()
        self.page.update()

    # def board_name_focus(self, e):
    #     e.control.read_only = False
    #     e.control.border = "outline"
    #     e.control.update()

    # def board_name_blur(self, e):
    #     self.store.update_board(
    #         self.store.get_boards()[e.control.data], {"name": e.control.value}
    #     )
    #     self.app_layout.hydrate_all_boards_view()
    #     e.control.read_only = True
    #     e.control.border = "none"
    #     self.page.update()

    def top_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        self.view.update()
        # sluggify label
        self.page.route = f"/{str(self.top_nav_items[index].label).lower()}"
        self.page.update()

    def bottom_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.top_nav_rail.selected_index = None
        self.bottom_nav_rail.selected_index = index
        self.page.route = f"/board/{index}"
        self.view.update()
        self.page.update()


class InMemoryStore(DataStore):
    def __init__(self):
        self.boards: dict[int, "Board"] = {}
        self.users: dict[str, "User"] = {}
        self.board_lists: dict[int, list["BoardList"]] = {}
        self.items: dict[int, list["Item"]] = {}

    # def add_board(self, board: "Board"):
    #     self.boards[board.board_id] = board

    # def get_board(self, id: int):
    #     return self.boards[id]

    # def update_board(self, board: "Board", update: dict):
    #     for k in update:
    #         setattr(board, k, update[k])

    # def get_boards(self):
    #     return [self.boards[b] for b in self.boards]

    # def remove_board(self, board: "Board"):
    #     del self.boards[board.board_id]
    #     self.board_lists[board.board_id] = []

    # def add_list(self, board: int, list: "BoardList"):
    #     if board in self.board_lists:
    #         self.board_lists[board].append(list)
    #     else:
    #         self.board_lists[board] = [list]

    # def get_lists_by_board(self, board: int):
    #     return self.board_lists.get(board, [])

    # def remove_list(self, board: int, id: int):
    #     self.board_lists[board] = [
    #         l for l in self.board_lists[board] if not l.board_list_id == id
    #     ]

    def add_user(self, user: "User"):
        self.users[user.name] = user

    def get_users(self):
        return [self.users[u] for u in self.users]

    # def add_item(self, board_list: int, item: "Item"):
    #     if board_list in self.items:
    #         self.items[board_list].append(item)
    #     else:
    #         self.items[board_list] = [item]

    # def get_items(self, board_list: int):
    #     return self.items.get(board_list, [])

    # def remove_item(self, board_list: int, id: int):
    #     self.items[board_list] = [
    #         i for i in self.items[board_list] if not i.item_id == id
    #     ]


# class Item(UserControl):
#     id_counter = itertools.count()

#     def __init__(self, list: "BoardList", store: DataStore, item_text: str):
#         super().__init__()
#         self.item_id = next(Item.id_counter)
#         self.store: DataStore = store
#         self.list = list
#         self.item_text = item_text
#         self.card_item = Card(
#             content=Row(
#                 [
#                     Container(
#                         content=Checkbox(label=f"{self.item_text}", width=200),
#                         border_radius=border_radius.all(5),
#                     )
#                 ],
#                 width=200,
#                 wrap=True,
#             ),
#             elevation=1,
#             data=self.list,
#         )

#     def build(self):

#         self.view = Draggable(
#             group="items",
#             content=DragTarget(
#                 group="items",
#                 content=self.card_item,
#                 on_accept=self.drag_accept,
#                 on_leave=self.drag_leave,
#                 on_will_accept=self.drag_will_accept,
#             ),
#             data=self,
#         )
#         return self.view

#     def drag_accept(self, e):
#         src = self.page.get_control(e.src_id)

#         # skip if item is dropped on itself
#         if src.content.content == e.control.content:
#             self.card_item.elevation = 1
#             self.list.set_indicator_opacity(self, 0.0)
#             e.control.update()
#             return

#         # item dropped within same list but not on self
#         if src.data.list == self.list:
#             self.list.add_item(chosen_control=src.data, swap_control=self)
#             self.card_item.elevation = 1
#             e.control.update()
#             return

#         # item added to different list
#         self.list.add_item(src.data.item_text, swap_control=self)
#         # remove from the list to which draggable belongs
#         src.data.list.remove_item(src.data)
#         self.list.set_indicator_opacity(self, 0.0)
#         self.card_item.elevation = 1
#         e.control.update()

#     def drag_will_accept(self, e):
#         if e.data == "true":
#             self.list.set_indicator_opacity(self, 1.0)
#         self.card_item.elevation = 20 if e.data == "true" else 1
#         e.control.update()

#     def drag_leave(self, e):
#         self.list.set_indicator_opacity(self, 0.0)
#         self.card_item.elevation = 1
#         e.control.update()


# class BoardList(UserControl):
#     id_counter = itertools.count()

#     def __init__(self, board: "Board", store: DataStore, title: str, color: str = ""):
#         super().__init__()
#         self.board_list_id = next(BoardList.id_counter)
#         self.store: DataStore = store
#         self.board = board
#         self.title = title
#         self.color = color
#         self.items = Column([], tight=True, spacing=4)
#         self.items.controls = self.store.get_items(self.board_list_id)

#     def build(self):

#         self.new_item_field = TextField(
#             label="new card name",
#             height=50,
#             bgcolor=colors.WHITE,
#             on_submit=self.add_item_handler,
#         )

#         self.end_indicator = Container(
#             bgcolor=colors.BLACK26,
#             border_radius=border_radius.all(30),
#             height=3,
#             width=200,
#             opacity=0.0,
#         )
#         self.edit_field = Row(
#             [
#                 TextField(
#                     value=self.title,
#                     width=150,
#                     height=40,
#                     content_padding=padding.only(left=10, bottom=10),
#                 ),
#                 TextButton(text="Save", on_click=self.save_title),
#             ]
#         )
#         self.header = Row(
#             controls=[
#                 Text(
#                     value=self.title,
#                     style="titleMedium",
#                     text_align="left",
#                     overflow="clip",
#                     expand=True,
#                 ),
#                 Container(
#                     PopupMenuButton(
#                         items=[
#                             PopupMenuItem(
#                                 content=Text(
#                                     value="Edit",
#                                     style="labelMedium",
#                                     text_align="center",
#                                     color=self.color,
#                                 ),
#                                 on_click=self.edit_title,
#                             ),
#                             PopupMenuItem(),
#                             PopupMenuItem(
#                                 content=Text(
#                                     value="Delete",
#                                     style="labelMedium",
#                                     text_align="center",
#                                     color=self.color,
#                                 ),
#                                 on_click=self.delete_list,
#                             ),
#                             PopupMenuItem(),
#                             PopupMenuItem(
#                                 content=Text(
#                                     value="Move List",
#                                     style="labelMedium",
#                                     text_align="center",
#                                     color=self.color,
#                                 )
#                             ),
#                         ],
#                     ),
#                     padding=padding.only(right=-10),
#                 ),
#             ],
#             alignment="spaceBetween",
#         )

#         self.inner_list = Container(
#             content=Column(
#                 [
#                     self.header,
#                     self.new_item_field,
#                     TextButton(
#                         content=Row(
#                             [Icon(icons.ADD), Text("add card", color=colors.BLACK38)],
#                             tight=True,
#                         ),
#                         on_click=self.add_item_handler,
#                     ),
#                     self.items,
#                     self.end_indicator,
#                 ],
#                 spacing=4,
#                 tight=True,
#                 data=self.title,
#             ),
#             width=250,
#             border=border.all(2, colors.BLACK12),
#             border_radius=border_radius.all(5),
#             bgcolor=self.color if (self.color != "") else colors.BACKGROUND,
#             padding=padding.only(bottom=10, right=10, left=10, top=5),
#         )
#         self.view = DragTarget(
#             group="items",
#             content=Draggable(
#                 group="lists",
#                 content=DragTarget(
#                     group="lists",
#                     content=self.inner_list,
#                     data=self,
#                     on_accept=self.list_drag_accept,
#                     on_will_accept=self.list_will_drag_accept,
#                     on_leave=self.list_drag_leave,
#                 ),
#             ),
#             data=self,
#             on_accept=self.item_drag_accept,
#             on_will_accept=self.item_will_drag_accept,
#             on_leave=self.item_drag_leave,
#         )

#         return self.view

#     def item_drag_accept(self, e):
#         src = self.page.get_control(e.src_id)
#         self.add_item(src.data.item_text)
#         src.data.list.remove_item(src.data)
#         self.end_indicator.opacity = 0.0
#         self.update()

#     def item_will_drag_accept(self, e):
#         if e.data == "true":
#             self.end_indicator.opacity = 1.0
#         self.update()

#     def item_drag_leave(self, e):
#         self.end_indicator.opacity = 0.0
#         self.update()

#     def list_drag_accept(self, e):
#         src = self.page.get_control(e.src_id)
#         l = self.board.board_lists
#         to_index = l.index(e.control.data)
#         from_index = l.index(src.content.data)
#         l[to_index], l[from_index] = l[from_index], l[to_index]
#         self.inner_list.border = border.all(2, colors.BLACK12)
#         self.board.update()
#         self.update()

#     def list_will_drag_accept(self, e):
#         if e.data == "true":
#             self.inner_list.border = border.all(2, colors.BLACK)
#         self.update()

#     def list_drag_leave(self, e):
#         self.inner_list.border = border.all(2, colors.BLACK12)
#         self.update()

#     def delete_list(self, e):
#         self.board.remove_list(self, e)

#     def edit_title(self, e):
#         self.header.controls[0] = self.edit_field
#         self.header.controls[1].visible = False
#         self.update()

#     def save_title(self, e):
#         self.title = self.edit_field.controls[0].value
#         self.header.controls[0] = Text(
#             value=self.title,
#             style="titleMedium",
#             text_align="left",
#             overflow="clip",
#             expand=True,
#         )

#         self.header.controls[1].visible = True
#         self.update()

#     def add_item_handler(self, e):
#         if self.new_item_field.value == "":
#             return
#         self.add_item()

#     def add_item(
#         self,
#         item: str = None,
#         chosen_control: Draggable = None,
#         swap_control: Draggable = None,
#     ):

#         controls_list = [x.controls[1] for x in self.items.controls]
#         to_index = (
#             controls_list.index(swap_control) if swap_control in controls_list else None
#         )
#         from_index = (
#             controls_list.index(chosen_control)
#             if chosen_control in controls_list
#             else None
#         )
#         control_to_add = Column(
#             [
#                 Container(
#                     bgcolor=colors.BLACK26,
#                     border_radius=border_radius.all(30),
#                     height=3,
#                     alignment=alignment.center_right,
#                     width=200,
#                     opacity=0.0,
#                 )
#             ]
#         )

#         # rearrange (i.e. drag drop from same list)
#         if (from_index is not None) and (to_index is not None):
#             self.items.controls.insert(to_index, self.items.controls.pop(from_index))
#             self.set_indicator_opacity(swap_control, 0.0)

#         # insert (drag from other list to middle of this list)
#         elif to_index is not None:
#             new_item = Item(self, self.store, item)
#             control_to_add.controls.append(new_item)
#             self.items.controls.insert(to_index, control_to_add)

#         # add new (drag from other list to end of this list, or use add item button)
#         else:
#             new_item = (
#                 Item(self, self.store, item)
#                 if item
#                 else Item(self, self.store, self.new_item_field.value)
#             )
#             control_to_add.controls.append(new_item)
#             self.items.controls.append(control_to_add)
#             self.store.add_item(self.board_list_id, new_item)
#             self.new_item_field.value = ""

#         self.view.update()
#         self.page.update()

#     def remove_item(self, item: Item):
#         controls_list = [x.controls[1] for x in self.items.controls]
#         del self.items.controls[controls_list.index(item)]
#         self.store.remove_item(self.board_list_id, item.item_id)
#         self.view.update()

#     def set_indicator_opacity(self, item, opacity):
#         controls_list = [x.controls[1] for x in self.items.controls]
#         self.items.controls[controls_list.index(item)].controls[0].opacity = opacity
#         self.view.update()


# class Board(UserControl):
#     id_counter = itertools.count()

#     def __init__(self, app, store: DataStore, name: str):
#         super().__init__()
#         self.board_id = next(Board.id_counter)
#         self.store: DataStore = store
#         self.app = app
#         self.name = name
#         self.add_list_button = FloatingActionButton(
#             icon=icons.ADD, text="add a list", height=30, on_click=self.create_list
#         )

#         self.board_lists = [self.add_list_button]
#         for l in self.store.get_lists_by_board(self.board_id):
#             self.add_list(l)

#         self.list_wrap = Row(
#             self.board_lists,
#             vertical_alignment="start",
#             visible=True,
#             scroll="auto",
#             width=(self.app.page.width - 310),
#             height=(self.app.page.height - 95),
#         )

#     def build(self):
#         self.view = Container(
#             content=Column(controls=[self.list_wrap], scroll="auto", expand=True),
#             data=self,
#             margin=margin.all(0),
#             padding=padding.only(top=10, right=0),
#             height=self.app.page.height,
#         )
#         return self.view

#     def resize(self, nav_rail_extended, width, height):
#         self.list_wrap.width = (width - 310) if nav_rail_extended else (width - 50)
#         self.view.height = height
#         self.list_wrap.update()
#         self.view.update()

#     def create_list(self, e):

#         option_dict = {
#             colors.LIGHT_GREEN: self.color_option_creator(colors.LIGHT_GREEN),
#             colors.RED_200: self.color_option_creator(colors.RED_200),
#             colors.AMBER_500: self.color_option_creator(colors.AMBER_500),
#             colors.PINK_300: self.color_option_creator(colors.PINK_300),
#             colors.ORANGE_300: self.color_option_creator(colors.ORANGE_300),
#             colors.LIGHT_BLUE: self.color_option_creator(colors.LIGHT_BLUE),
#             colors.DEEP_ORANGE_300: self.color_option_creator(colors.DEEP_ORANGE_300),
#             colors.PURPLE_100: self.color_option_creator(colors.PURPLE_100),
#             colors.RED_700: self.color_option_creator(colors.RED_700),
#             colors.TEAL_500: self.color_option_creator(colors.TEAL_500),
#             colors.YELLOW_400: self.color_option_creator(colors.YELLOW_400),
#             colors.PURPLE_400: self.color_option_creator(colors.PURPLE_400),
#             colors.BROWN_300: self.color_option_creator(colors.BROWN_300),
#             colors.CYAN_500: self.color_option_creator(colors.CYAN_500),
#             colors.BLUE_GREY_500: self.color_option_creator(colors.BLUE_GREY_500),
#         }

#         def set_color(e):
#             color_options.data = e.control.data
#             for k, v in option_dict.items():
#                 if k == e.control.data:
#                     v.border = border.all(3, colors.BLACK26)
#                 else:
#                     v.border = None
#             dialog.content.update()

#         color_options = GridView(runs_count=3, max_extent=40, data="", height=150)

#         for _, v in option_dict.items():
#             v.on_click = set_color
#             color_options.controls.append(v)

#         def close_dlg(e):
#             if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
#                 type(e.control) is TextField and e.control.value != ""
#             ):
#                 new_list = BoardList(
#                     self, self.store, dialog_text.value, color=color_options.data
#                 )
#                 self.add_list(new_list)
#             dialog.open = False
#             self.page.update()
#             self.update()

#         def textfield_change(e):
#             if dialog_text.value == "":
#                 create_button.disabled = True
#             else:
#                 create_button.disabled = False
#             self.page.update()

#         dialog_text = TextField(
#             label="New List Name", on_submit=close_dlg, on_change=textfield_change
#         )
#         create_button = ElevatedButton(
#             text="Create", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True
#         )
#         dialog = AlertDialog(
#             title=Text("Name your new list"),
#             content=Column(
#                 [
#                     Container(
#                         content=dialog_text, padding=padding.symmetric(horizontal=5)
#                     ),
#                     color_options,
#                     Row(
#                         [
#                             ElevatedButton(text="Cancel", on_click=close_dlg),
#                             create_button,
#                         ],
#                         alignment="spaceBetween",
#                     ),
#                 ],
#                 tight=True,
#                 alignment="center",
#             ),
#             on_dismiss=lambda e: print("Modal dialog dismissed!"),
#         )
#         self.page.dialog = dialog
#         dialog.open = True
#         self.page.update()
#         dialog_text.focus()

#     def remove_list(self, list: BoardList, e):
#         self.board_lists.remove(list)
#         self.store.remove_list(self.board_id, list.board_list_id)
#         self.update()

#     def add_list(self, list: BoardList):
#         self.board_lists.insert(-1, list)
#         self.store.add_list(self.board_id, list)

#     def color_option_creator(self, color: str):
#         return Container(
#             bgcolor=color,
#             border_radius=border_radius.all(50),
#             height=10,
#             width=10,
#             padding=padding.all(5),
#             alignment=alignment.center,
#             data=color,
#         )


class AppLayout(Row):
    def __init__(self, app, page: Page, store: DataStore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.page.on_resize = self.page_resize
        self.store: DataStore = store
        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.sidebar = Sidebar(self, self.store, page)
        self.members_view = Text("members view")
        # self.all_boards_view = Column(
        #     [
        #         Row(
        #             [
        #                 Container(
        #                     Text(value="Your Boards", style="headlineMedium"),
        #                     expand=True,
        #                     padding=padding.only(top=15),
        #                 ),
        #                 Container(
        #                     TextButton(
        #                         "Add new board",
        #                         icon=icons.ADD,
        #                         # on_click=self.app.add_board,
        #                         style=ButtonStyle(
        #                             bgcolor={
        #                                 "": colors.BLUE_200,
        #                                 "hovered": colors.BLUE_400,
        #                             },
        #                             shape={"": RoundedRectangleBorder(radius=3)},
        #                         ),
        #                     ),
        #                     padding=padding.only(right=50, top=15),
        #                 ),
        #             ]
        #         ),
        #         Row(
        #             [
        #                 TextField(
        #                     hint_text="Search all boards",
        #                     autofocus=False,
        #                     content_padding=padding.only(left=10),
        #                     width=200,
        #                     height=40,
        #                     text_size=12,
        #                     border_color=colors.BLACK26,
        #                     focused_border_color=colors.BLUE_ACCENT,
        #                     suffix_icon=icons.SEARCH,
        #                 )
        #             ]
        #         ),
        #         Row([Text("No Boards to Display")]),
        #     ],
        #     expand=True,
        # )
        self._active_view: Control = Column()

        self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.sidebar.sync_board_destinations()
        self.update()

    # def set_board_view(self, i):
    #     self.active_view = self.store.get_boards()[i]
    #     self.sidebar.bottom_nav_rail.selected_index = i
    #     self.sidebar.top_nav_rail.selected_index = None
    #     self.sidebar.update()
    #     self.page.update()
    #     self.page_resize()

    # def set_all_boards_view(self):
    #     self.active_view = self.all_boards_view
    #     self.hydrate_all_boards_view()
    #     self.sidebar.top_nav_rail.selected_index = 0
    #     self.sidebar.bottom_nav_rail.selected_index = None
    #     self.sidebar.update()
    #     self.page.update()

    # def set_members_view(self):
    #     self.active_view = self.members_view
    #     self.sidebar.top_nav_rail.selected_index = 1
    #     self.sidebar.bottom_nav_rail.selected_index = None
    #     self.sidebar.update()
    #     self.page.update()

    def set_dynamic_view(self, view):
        self.active_view = view.main(self.page)
        # self.sidebar.top_nav_rail.selected_index = 1
        # self.sidebar.bottom_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()

    def page_resize(self, e=None):
        # if type(self.active_view) is Board:
        #     self.active_view.resize(
        #         self.sidebar.visible, self.page.width, self.page.height
        #     )
        # self.page.update()
        pass

    # def hydrate_all_boards_view(self):
    #     self.all_boards_view.controls[-1] = Row(
    #         [
    #             Container(
    #                 content=Row(
    #                     [
    #                         Container(
    #                             content=Text(value=b.name),
    #                             data=b,
    #                             expand=True,
    #                             on_click=self.board_click,
    #                         ),
    #                         Container(
    #                             content=PopupMenuButton(
    #                                 items=[
    #                                     PopupMenuItem(
    #                                         content=Text(
    #                                             value="Delete",
    #                                             style="labelMedium",
    #                                             text_align="center",
    #                                         ),
    #                                         on_click=self.app.delete_board,
    #                                         data=b,
    #                                     ),
    #                                     PopupMenuItem(),
    #                                     PopupMenuItem(
    #                                         content=Text(
    #                                             value="Archive",
    #                                             style="labelMedium",
    #                                             text_align="center",
    #                                         ),
    #                                     ),
    #                                 ]
    #                             ),
    #                             padding=padding.only(right=-10),
    #                             border_radius=border_radius.all(3),
    #                         ),
    #                     ],
    #                     alignment="spaceBetween",
    #                 ),
    #                 border=border.all(1, colors.BLACK38),
    #                 border_radius=border_radius.all(5),
    #                 bgcolor=colors.WHITE60,
    #                 padding=padding.all(10),
    #                 width=250,
    #                 data=b,
    #             )
    #             for b in self.store.get_boards()
    #         ],
    #         wrap=True,
    #     )
    #     self.sidebar.sync_board_destinations()

    # def board_click(self, e):
    #     self.sidebar.bottom_nav_change(self.store.get_boards().index(e.control.data))

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page_resize()
        self.page.update()


class Player1Client(UserControl):
    def __init__(self, page: Page, store: DataStore):
        super().__init__()
        self.page = page
        self.store: DataStore = store  # customisable
        self.page.on_route_change = self.route_change
        # self.boards = self.store.get_boards()
        self.login_profile_button = PopupMenuItem(text="Log in", on_click=self.login)
        self.appbar_items = [
            self.login_profile_button,
            PopupMenuItem(),  # divider
            PopupMenuItem(text="About"),
            PopupMenuItem(text="Settings"),
        ]
        self.appbar = AppBar(
            leading=Icon(icons.TERMINAL),
            leading_width=100,
            title=Text(f"Player1Client", size=32, text_align="start"),
            center_title=True,
            toolbar_height=75,
            bgcolor=colors.BLUE_GREY_900,
            actions=[
                Container(
                    content=PopupMenuButton(items=self.appbar_items),
                    margin=margin.only(left=50, right=25),
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            self.store,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )
        return self.layout

    def initialize(self):
        self.page.views.append(
            View(
                "/",
                [self.appbar, self.layout],
                padding=padding.all(0),
                bgcolor=colors.BLACK,
            )
        )
        self.page.update()
        # create an initial board for demonstration if no boards
        # if len(self.boards) == 0:
        #     self.create_new_board("My First Board")
        # self.page.go("/")

    def login(self, e):
        def close_dlg(e):
            if user_name.value == "" or password.value == "":
                user_name.error_text = "Please provide username"
                password.error_text = "Please provide password"
                self.page.update()
                return
            else:
                user = User(user_name.value, password.value)
                if user not in self.store.get_users():
                    self.store.add_user(user)
                self.user = user_name.value
                self.page.client_storage.set("current_user", user_name.value)

            dialog.open = False
            self.appbar_items[0] = PopupMenuItem(
                text=f"{self.page.client_storage.get('current_user')}'s Profile"
            )
            self.page.update()

        user_name = TextField(label="User name")
        password = TextField(label="Password", password=True)
        dialog = AlertDialog(
            title=Text("Please enter your login credentials"),
            content=Column(
                [
                    user_name,
                    password,
                    ElevatedButton(text="Login", on_click=close_dlg),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        # if troute.match("/board/:id"):
        #     if int(troute.id) > len(self.store.get_boards()):
        #         self.page.go("/boards")
        #         return
        #     self.layout.set_board_view(int(troute.id))
        # elif troute.match("/boards"):
        #     self.layout.set_all_boards_view()
        # elif troute.match("/members"):
        #     self.layout.set_members_view()
        # else:
        page_route = (
            troute.route[1:].split("/")[0]
            if troute.route.startswith("/") and len(troute.route) > 1
            else "home"
        )
        try:
            # view = importlib.import_module(f"player1dev.views.{page_route}")
            # Client views and fallback to module folder
            view = importlib.import_module(f"views.{page_route}")
            self.layout.set_dynamic_view(view)

        except (ModuleNotFoundError):
            view = importlib.import_module(f"player1dev.views.error404")
            self.layout.set_dynamic_view(view)
        except:
            view = importlib.import_module(f"player1dev.views.error500")
            self.layout.set_dynamic_view(view)
        self.page.update()

    # def add_board(self, e):
    #     def close_dlg(e):
    #         if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
    #             type(e.control) is TextField and e.control.value != ""
    #         ):
    #             self.create_new_board(dialog_text.value)
    #         dialog.open = False
    #         self.page.update()

    #     def textfield_change(e):
    #         if dialog_text.value == "":
    #             create_button.disabled = True
    #         else:
    #             create_button.disabled = False
    #         self.page.update()

    #     dialog_text = TextField(
    #         label="New Board Name", on_submit=close_dlg, on_change=textfield_change
    #     )
    #     create_button = ElevatedButton(
    #         text="Create", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True
    #     )
    #     dialog = AlertDialog(
    #         title=Text("Name your new board"),
    #         content=Column(
    #             [
    #                 dialog_text,
    #                 Row(
    #                     [
    #                         ElevatedButton(text="Cancel", on_click=close_dlg),
    #                         create_button,
    #                     ],
    #                     alignment="spaceBetween",
    #                 ),
    #             ],
    #             tight=True,
    #         ),
    #         on_dismiss=lambda e: print("Modal dialog dismissed!"),
    #     )
    #     self.page.dialog = dialog
    #     dialog.open = True
    #     self.page.update()
    #     dialog_text.focus()

    # def create_new_board(self, board_name):
    #     new_board = Board(self, self.store, board_name)
    #     self.store.add_board(new_board)
    #     self.layout.hydrate_all_boards_view()

    # def delete_board(self, e):
    #     self.store.remove_board(e.control.data)
    #     self.layout.set_all_boards_view()


if __name__ == "__main__":

    def main(page: Page):
        page.title = "Player1Client"
        page.padding = 0
        page.theme = theme.Theme(font_family="Verdana")
        # page.theme.page_transitions.windows = "cupertino"
        # page.fonts = {"Pacifico": "/Pacifico-Regular.ttf"}
        page.bgcolor = colors.BLUE_GREY_900
        page.window_bgcolor = colors.BLUE_GREY_900
        app = Player1Client(page, InMemoryStore())
        page.add(app)
        page.update()
        app.initialize()

    flet.app(target=main, assets_dir="../assets", route_url_strategy="path")
