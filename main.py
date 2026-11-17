import flet as ft
import pymysql

def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="admin",
        password="12345",
        database="sistema_gimnasio",
        cursorclass=pymysql.cursors.DictCursor
    )

def main(page: ft.Page):
    page.title = "IRON GYM - Sistema de Gestión"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.padding = 20
    page.scroll = "adaptive"

    txt_total = ft.Text("0", size=28, weight="bold", color="#38BDF8")
    txt_activos = ft.Text("0", size=28, weight="bold", color="#4ADE80")
    txt_vencidos = ft.Text("0", size=28, weight="bold", color="#F87171")

    input_nombre = ft.TextField(label="Nombre Completo", border_color="#38BDF8", expand=True)
    input_telefono = ft.TextField(label="Teléfono / WhatsApp", border_color="#38BDF8", width=200)
    dropdown_plan = ft.Dropdown(
        label="Plan de Membresía",
        width=220,
        border_color="#38BDF8",
        options=[
            ft.dropdown.Option("Mensual Básico"),
            ft.dropdown.Option("Mensual VIP"),
            ft.dropdown.Option("Trimestral"),
            ft.dropdown.Option("Anual Pro"),
        ],
        value="Mensual Básico"
    )

    tabla_miembros = ft.DataTable(
        border=ft.border.all(1, "#334155"),
        border_radius=10,
        heading_row_color="#1E293B",
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold")),
            ft.DataColumn(ft.Text("Miembro", weight="bold")),
            ft.DataColumn(ft.Text("Teléfono", weight="bold")),
            ft.DataColumn(ft.Text("Plan", weight="bold")),
            ft.DataColumn(ft.Text("Estado", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        rows=[]
    )

    def mostrar_alerta(mensaje, color="#4ADE80"):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje, color="black", weight="bold"), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def cargar_datos():
        try:
            conn = conectar_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM miembros ORDER BY id DESC")
                registros = cursor.fetchall()
            conn.close()

            tabla_miembros.rows.clear()
            activos = 0
            vencidos = 0

            for r in registros:
                if r["estado"] == "Activo":
                    activos += 1
                    badge_color = "#166534"
                    text_color = "#4ADE80"
                else:
                    vencidos += 1
                    badge_color = "#991B1B"
                    text_color = "#F87171"

                tabla_miembros.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(r["id"]))),
                            ft.DataCell(ft.Text(r["nombre"], weight="w500")),
                            ft.DataCell(ft.Text(r["telefono"])),
                            ft.DataCell(ft.Text(r["plan"])),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(r["estado"], size=12, color=text_color, weight="bold"),
                                    bgcolor=badge_color,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                    border_radius=15
                                )
                            ),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.SWAP_HORIZ,
                                        icon_color="#38BDF8",
                                        tooltip="Cambiar Estado",
                                        on_click=lambda e, id_m=r["id"], est=r["estado"]: cambiar_estado(id_m, est)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color="#F87171",
                                        tooltip="Eliminar",
                                        on_click=lambda e, id_m=r["id"]: eliminar_miembro(id_m)
                                    )
                                ])
                            )
                        ]
                    )
                )

            txt_total.value = str(len(registros))
            txt_activos.value = str(activos)
            txt_vencidos.value = str(vencidos)
            page.update()
        except Exception as ex:
            mostrar_alerta(f"Error de BD: {ex}", "#F87171")

    def agregar_miembro(e):
        if not input_nombre.value or not input_telefono.value:
            mostrar_alerta("Completa nombre y teléfono", "#FBBF24")
            return
        try:
            conn = conectar_db()
            with conn.cursor() as cursor:
                sql = "INSERT INTO miembros (nombre, telefono, plan, estado) VALUES (%s, %s, %s, 'Activo')"
                cursor.execute(sql, (input_nombre.value, input_telefono.value, dropdown_plan.value))
            conn.commit()
            conn.close()

            input_nombre.value = ""
            input_telefono.value = ""
            mostrar_alerta("¡Miembro registrado con éxito!")
            cargar_datos()
        except Exception as ex:
            mostrar_alerta(f"Error al guardar: {ex}", "#F87171")

    def cambiar_estado(id_miembro, estado_actual):
        nuevo_estado = "Vencido" if estado_actual == "Activo" else "Activo"
        conn = conectar_db()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE miembros SET estado = %s WHERE id = %s", (nuevo_estado, id_miembro))
        conn.commit()
        conn.close()
        cargar_datos()

    def eliminar_miembro(id_miembro):
        conn = conectar_db()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM miembros WHERE id = %s", (id_miembro,))
        conn.commit()
        conn.close()
        mostrar_alerta("Miembro eliminado", "#F87171")
        cargar_datos()

    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.FITNESS_CENTER, size=36, color="#38BDF8"),
            ft.Column([
                ft.Text("IRON GYM CONTROL", size=24, weight="bold", color="white"),
                ft.Text("Panel de Administración en VPS", size=13, color="#94A3B8")
            ], spacing=0)
        ]),
        padding=ft.padding.only(bottom=15)
    )

    def tarjeta_metrica(titulo, control_numero, icono, color_borde):
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(titulo, size=14, color="#94A3B8"),
                    control_numero
                ]),
                ft.Icon(icono, size=36, color=color_borde)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor="#1E293B",
            padding=20,
            border_radius=12,
            border=ft.border.only(left=ft.BorderSide(4, color_borde)),
            expand=True
        )

    fila_metricas = ft.Row([
        tarjeta_metrica("Total Miembros", txt_total, ft.Icons.GROUPS, "#38BDF8"),
        tarjeta_metrica("Membresías Activas", txt_activos, ft.Icons.CHECK_CIRCLE, "#4ADE80"),
        tarjeta_metrica("Membresías Vencidas", txt_vencidos, ft.Icons.WARNING_AMBER, "#F87171"),
    ], spacing=15)

    panel_registro = ft.Container(
        content=ft.Column([
            ft.Text("Registrar Nuevo Socio", size=16, weight="bold", color="#38BDF8"),
            ft.Row([
                input_nombre,
                input_telefono,
                dropdown_plan,
                ft.ElevatedButton(
                    "Registrar",
                    icon=ft.Icons.PERSON_ADD,
                    bgcolor="#0284C7",
                    color="white",
                    height=50,
                    on_click=agregar_miembro
                )
            ], wrap=True)
        ]),
        bgcolor="#1E293B",
        padding=20,
        border_radius=12
    )

    page.add(
        header,
        fila_metricas,
        ft.Divider(height=20, color="transparent"),
        panel_registro,
        ft.Divider(height=20, color="transparent"),
        ft.Text("Directorio de Socios", size=18, weight="bold"),
        ft.Container(content=tabla_miembros, expand=True)
    )

    cargar_datos()

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="0.0.0.0")
