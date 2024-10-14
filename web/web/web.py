"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .components.navbar import navbar
from .pages.replication_page import replication
from .state import State


color = "rgb(107,99,246)"

def upload_box() -> rx.Component:
    return  rx.upload(
        rx.vstack(
            rx.button(
                "Subir archivo Fasta",
                color=color,
                bg="white",
                border=f"1px solid {color}",
            ),
            rx.text(
                "Selecciona el archivo con la secuencia a replicar"
            ),
        ),
        id="upload1",
        border=f"1px dotted {color}",
        padding="5em",
    ), rx.hstack(
        rx.foreach(
            rx.selected_files("upload1"), rx.text
        )
    ),  rx.flex(
        rx.button(
            "Subir",
            on_click=State.handle_upload(rx.upload_files(upload_id="upload1")),
        ),
        rx.button(
            "Borrar",
            on_click=rx.clear_selected_files("upload1"),
        ),
        justify="center",
        gap="10px",
    ), rx.divider(width="100%"),


def box_generate_random_adn() -> rx.Component:
    return rx.vstack(
        rx.form.root(
            rx.vstack(
                rx.heading("Generar cadena de ADN aleatoria", size="5"),
                rx.input(
                    name="input",
                    default_value="10",
                    placeholder="Tamaño cadena de ADN aleatoria",
                ),
                rx.button("Generar", type="submit"),
                width="100%",
            ),
            on_submit=State.handle_generate_adn,
            reset_on_submit=True,
            width="100%",
        ),
        rx.divider(width="100%"),
        rx.heading("Cadena de ADN:", size="5"),
        rx.text(State.content),
        width="100%",
    )

@rx.page(route="/upload-data")
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.fragment(  # Asegúrate de devolver el componente aquí
        navbar(),
        rx.container(
            rx.color_mode.button(position="bottom-right"),
            rx.vstack(
                rx.heading("¡Bienvenido al simulador de replicación de ADN!", size="9"),
                rx.text(
                    "Selecciona tu secuencia de ADN",
                    size="5",
                ),
                upload_box(),
                box_generate_random_adn(),
                spacing="5",
                justify="center",
                min_height="35vh",
            ),
        )
    )


app = rx.App(
    stylesheets=["/custom_violet.css"],
    theme = rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="blue",
    ), 
)
app.add_page(index)
app.add_page(replication)
