import flet as ft
from ChatClient import ChatClient

client = ChatClient()

def main(page: ft.Page):
    page.title = "Chat Client"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username_input = ft.Ref[ft.TextField]()
    password_input = ft.Ref[ft.TextField]()
    name_input = ft.Ref[ft.TextField]()
    country_input = ft.Ref[ft.TextField]()
    groupname_input = ft.Ref[ft.TextField]()
    usernameto_input = ft.Ref[ft.TextField]()
    message_input = ft.Ref[ft.TextField]()
    filepath_input = ft.Ref[ft.TextField]()

    realmname_input = ft.Ref[ft.TextField]()
    realmaddress_input = ft.Ref[ft.TextField]()
    realmport_input = ft.Ref[ft.TextField]()

    output = ft.Ref[ft.Text]()

    # view login page
    def show_login_page(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Username", width=300, ref=username_input),
                    ft.TextField(label="Password", password=True, width=300, ref=password_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Login", on_click=on_login_click),
                            ft.ElevatedButton(text="Register", on_click=show_register_page),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view register page
    def show_register_page(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Username", width=300, ref=username_input),
                    ft.TextField(label="Password", password=True, width=300, ref=password_input),
                    ft.TextField(label="Name", width=300, ref=name_input),
                    ft.TextField(label="Country", width=300, ref=country_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Login", on_click=show_login_page),
                            ft.ElevatedButton(text="Register", on_click=on_register_click),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view main menu page
    def show_main_menu(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(text="Private Messaging", on_click=show_private_messaging),
                    ft.ElevatedButton(text="Group Messaging", on_click=show_group_messaging),
                    ft.ElevatedButton(text="Add Realm", on_click=show_add_realm),
                    ft.ElevatedButton(text="Private Realm Messaging", on_click=show_private_realm_messaging),
                    ft.ElevatedButton(text="Group Realm Messaging", on_click=show_group_realm_messaging),
                    ft.ElevatedButton(text="Check Inbox", on_click=show_inbox),
                    ft.ElevatedButton(text="User info", on_click=show_user_info),
                    # ft.ElevatedButton(text="Logout", on_click=logout),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view private messaage (in one realm)
    def show_private_messaging(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Send To (Username)", width=300, ref=usernameto_input),
                    ft.TextField(label="Message", width=300, ref=message_input),
                    ft.TextField(label="File Path", width=300, ref=filepath_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Send Message", on_click=on_send_message_click),
                            ft.ElevatedButton(text="Send File", on_click=on_send_file_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view private message (multirealm)
    def show_private_realm_messaging(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Realm Name", width=300, ref=realmname_input),
                    ft.TextField(label="Send To (Username)", width=300, ref=usernameto_input),
                    ft.TextField(label="Message", width=300, ref=message_input),
                    ft.TextField(label="File Path", width=300, ref=filepath_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Send Private Realm Message", on_click=on_send_realm_message_click),
                            ft.ElevatedButton(text="Send Private Realm File", on_click=on_send_realm_file_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view group messaging (in one realm)
    def show_group_messaging(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Send To (Group)", width=300, ref=groupname_input),
                    ft.TextField(label="Message", width=300, ref=message_input),
                    ft.TextField(label="File Path", width=300, ref=filepath_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Send Message", on_click=on_send_message_group_click),
                            ft.ElevatedButton(text="Send File", on_click=on_send_file_group_click),
                            ft.ElevatedButton(text="Add New Group", on_click=show_new_group),
                            ft.ElevatedButton(text="Join Group", on_click=show_join_group),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view group messaging (multirealm)
    def show_group_realm_messaging(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Realm Name", width=300, ref=realmname_input),
                    ft.TextField(label="Send To (ex: \"username1, username2\" or \"group:groupname\")", width=300, ref=groupname_input),
                    ft.TextField(label="Message", width=300, ref=message_input),
                    ft.TextField(label="File Path", width=300, ref=filepath_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Send Group Realm Message", on_click=on_send_message_group_realm_click),
                            ft.ElevatedButton(text="Send Group Realm File", on_click=on_send_file_group_realm_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view adding group
    def show_new_group(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Group Name", width=300, ref=groupname_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Make Group", on_click=on_make_group_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Group Messaging", on_click=show_group_messaging),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view adding realm
    def show_add_realm(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Realm Name", width=300, ref=realmname_input),
                    ft.TextField(label="Realm Address", width=300, ref=realmaddress_input),
                    ft.TextField(label="Realm Port", width=300, ref=realmport_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Make Realm", on_click=on_make_realm_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view getrealminbox
    def show_check_realm_inbox(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Realm Name", width=300, ref=realmname_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Check Inbox from this Realm", on_click=on_realm_inbox_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Inbox", on_click=show_inbox),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
    
    # view join group
    def show_join_group(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Group Name", width=300, ref=groupname_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Join Group", on_click=on_join_group_click)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton(text="Back to Group Messaging", on_click=show_group_messaging),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view check inbox
    def show_inbox(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Check Inbox", on_click=check_inbox),
                            ft.ElevatedButton(text="Check Realm Inbox", on_click=show_check_realm_inbox),
                            ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # view user info
    def show_user_info(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(text="User Info", on_click=check_info),
                            ft.ElevatedButton(text="Back to Menu", on_click=show_main_menu)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="Output will appear here", ref=output),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
    
    def handle_auth_result(result):
        output.current.value = result
        output.current.update()
        if "ok" in result.lower():
            show_main_menu()

    def handle_register_result(result):
        output.current.value = result
        output.current.update()
        if "ok" in result.lower():
            show_login_page()

    def on_login_click(e):
        username = username_input.current.value
        password = password_input.current.value
        result = client.proses(f"auth {username} {password}")
        handle_auth_result(result)

    def on_register_click(e):
        username = username_input.current.value
        password = password_input.current.value
        name = name_input.current.value
        country = country_input.current.value
        result = client.proses(f"register {username} {password} {name} {country}")
        handle_register_result(result)

    def on_send_message_click(e):
        usernameto = usernameto_input.current.value
        message = message_input.current.value
        result = client.proses(f"send {usernameto} {message}")
        output.current.value = result
        output.current.update()

    def on_send_realm_message_click(e):
        realmname = realmname_input.current.value
        usernameto = usernameto_input.current.value
        message = message_input.current.value
        result = client.proses(f"sendprivaterealm {realmname} {usernameto} {message}") 
        output.current.value = result
        output.current.update()

    def on_send_file_click(e):
        usernameto = usernameto_input.current.value
        filepath = filepath_input.current.value
        result = client.proses(f"sendfile {usernameto} {filepath}")
        output.current.value = result
        output.current.update()

    def on_send_realm_file_click(e):
        realmname = realmname_input.current.value
        usernameto = usernameto_input.current.value
        filepath = filepath_input.current.value
        result = client.proses(f"sendfilerealm {realmname} {usernameto} {filepath}")
        output.current.value = result
        output.current.update()

    def on_send_message_group_click(e):
        groupname = groupname_input.current.value
        message = message_input.current.value
        result = client.proses(f"sendgroup {groupname} {message}")
        output.current.value = result
        output.current.update()
    
    def on_send_message_group_realm_click(e):
        realmname = realmname_input.current.value
        groupname = groupname_input.current.value
        message = message_input.current.value
        result = client.proses(f"sendgrouprealm {realmname} {groupname} {message}")
        output.current.value = result
        output.current.update()

    def on_send_file_group_click(e):
        groupname = groupname_input.current.value
        filepath = filepath_input.current.value
        result = client.proses(f"sendgroupfile {groupname} {filepath}")
        output.current.value = result
        output.current.update()

    def on_send_file_group_realm_click(e):
        realmname = realmname_input.current.value
        groupname = groupname_input.current.value
        filepath = filepath_input.current.value
        result = client.proses(f"sendgroupfilerealm {realmname} {groupname} {filepath}")
        output.current.value = result
        output.current.update()

    def on_make_group_click(e):
        groupname = groupname_input.current.value
        result = client.proses(f"addgroup {groupname}")
        output.current.value = result
        output.current.update()

    def on_make_realm_click(e):
        realmname = realmname_input.current.value
        realmaddress = realmaddress_input.current.value
        realmport = realmport_input.current.value
        result = client.proses(f"addrealm {realmname} {realmaddress} {realmport}")
        output.current.value = result
        output.current.update()

    def on_join_group_click(e):
        groupname = groupname_input.current.value
        result = client.proses(f"joingroup {groupname}")
        output.current.value = result
        output.current.update()

    def check_inbox(e):
        result = client.proses(f"inbox")
        output.current.value = result
        output.current.update()

    def on_realm_inbox_click(e):
        realmname = realmname_input.current.value
        result = client.proses(f"getrealminbox {realmname}")
        output.current.value = result
        output.current.update()

    # def logout(e):
    #     result = client.proses(f"auth {username} {password}")
    #     if "ok" in result.lower():
    #         show_login_page()

    def check_info(e):
        result = client.proses(f"info")
        output.current.value = result
        output.current.update()

    show_login_page()

ft.app(target=main)
