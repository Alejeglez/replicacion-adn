import reflex as rx
from rxconfig import config
from ..components.navbar import navbar
from ..state import State

def divider():
    return rx.box(height="2px", width="100%", bg="#ccc", margin="20px 0")

common_style = {
    "backgroundColor": "white",  # Fondo blanco
    "color": "black",            # Letras negras
    "padding": "10px",           # Mantener el padding
    "borderRadius": "5px"        # Mantener el borde redondeado
}

code_helicasa = """def helicasa_action(self, i):
    self.chain_1_processed.append(self.chain_1[i])
    self.chain_2_processed.append(self.chain_2[i])

    self.position_helicasa = i

    chain_1_str = "".join(self.chain_1_processed)
    chain_2_str = "".join(self.chain_2_processed)"""

code_topoisomerasa = """def topoisomerasa_action(self):
    text = f"La topoisomerasa ha comenzado a actuar para aliviar la tensión generada por la helicasa.\n\n"
    print(text)"""

code_ssb = """def bind_ssb(self, position):
    text = f"Proteínas SSB unidas a las posiciones {position - 2} a {position} en ambas hebras.\n\n"
    print(text)"""

code_primasa_leader = """def activate_cebador_lider(self):
    base_comp = self.get_complementary_base(self.pairs_adn_arn_comp ,self.chain_1_processed[self.position_helicasa - 1])
    self.cebador_lider.append(base_comp)
    self.new_comp_chain_1.append(base_comp)"""

code_primasa_lagger = """def activate_cebador_rezagado(self):
    base_comp = self.get_complementary_base(self.pairs_adn_arn_comp, self.chain_2_processed[self.position_helicasa - 1])
    self.cebador_rezagado.append(base_comp)
    self.new_comp_chain_2.append(base_comp)
    self.rezagado_cebador_positions.append(self.position_helicasa - 1)"""

code_adn_polimerasa_III_leader = """def adn_polimerasa_lider_action(self):
    if len(self.new_comp_chain_1) < len(self.chain_1_processed) -1:
        base_comp = self.get_complementary_base(self.pairs_adn_adn_comp, self.chain_1_processed[self.position_helicasa - 1])
        self.new_comp_chain_1.append(base_comp)


    elif len(self.new_comp_chain_1) == len(self.chain_1_processed) - 1:
        base_comp = self.get_complementary_base(self.pairs_adn_adn_comp, self.chain_1_processed[self.position_helicasa])
        self.new_comp_chain_1.append(base_comp)

    elif len(self.new_comp_chain_1) == len(self.chain_1_processed):
        text = f"La ADN polimerasa III líder ha terminado de replicar la cadena de ADN líder.\n\n"
"""

code_adn_polimersa_rezagado = """def adn_polimerasa_rezagado_action(self):
    if len(self.new_comp_chain_2) < len(self.chain_2_processed) - 1:
        base_comp = self.get_complementary_base(
            self.pairs_adn_adn_comp, self.chain_2_processed[self.position_helicasa - 1]
        )
        self.new_comp_chain_2.append(base_comp)
    
    elif len(self.new_comp_chain_2) == len(self.chain_2_processed) - 1:
        base_comp = self.get_complementary_base(
            self.pairs_adn_adn_comp, self.chain_2_processed[self.position_helicasa]
        )
        self.new_comp_chain_2.append(base_comp)
    
    elif len(self.new_comp_chain_2) == len(self.chain_2_processed):
        text = f"La ADN polimerasa III rezagada ha terminado de replicar la cadena de ADN rezagada.\n\nSe han sintetizado {self.n_fragmentos_okazaki} fragmentos de Okazaki."
        self.replicated = True
"""

code_replace_primers_with_dna = """def replace_primers_with_dna(self):
    for i in range(len(self.cebador_lider)):
        base = self.cebador_lider[i]
        self.new_comp_chain_1[i] = self.pairs_arn_adn[base]

    for position in self.rezagado_cebador_positions:
        self.new_comp_chain_2[position] = self.get_complementary_base(
            self.pairs_arn_adn, self.new_comp_chain_2[position]
        )"""

code_ligase_action = """def ligase_action(self):

    return "".join(self.new_comp_chain_1), "".join(self.new_comp_chain_2)"""

code_replication = """def start_replication(self):
    i = 0

    while not self.replicated:
        if i < len(self.adn):
            self.helicasa_action(i)

        if self.position_helicasa == 1:
            self.topoisomerasa_action()

        if (self.position_helicasa + 1) % 3 == 0:
            self.bind_ssb(self.position_helicasa + 1)

        if self.position_helicasa > 0:
            self.replicate_lider()
            self.replicate_rezagada()
        i += 1

    self.replace_primers_with_dna()
    replicated_leader, replicated_lagger = self.ligase_action()"""

code_replication_leader = """def replicate_lider(self):
    if self.position_helicasa < 11:
        self.activate_cebador_lider()
    else:
        self.adn_polimerasa_lider_action()"""

code_replication_lagger = """def replicate_rezagada(self):
    if self.cebador_rezagado == []:
        self.activate_cebador_rezagado()
    else:
        self.adn_polimerasa_rezagada_action()
        if (self.position_helicasa - 1) - self.rezagado_cebador_positions[-1] == 3:
            self.cebador_rezagado = []
            self.n_fragmentos_okazaki += 1"""

@rx.page(route="/replication")
def replication() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.container(
            rx.cond(
                State.file_uploaded,
                rx.box(
                    rx.heading(
                        "Replicación del ADN",
                        size="7",
                    ),
                    rx.section(
                        rx.heading("Fase de iniciación", size="5"),
                        rx.markdown(State.text["fase_iniciación"]), 
                        rx.accordion.root(
                            rx.accordion.item(
                                header="Helicasa",
                                content=rx.box(
                                    rx.markdown(State.text["helicasa_info"]),
                                    rx.heading("Ejemplo inicio", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["helicasa_action_1"]),
                                        style=common_style  # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Ejemplo final", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["helicasa_action_2"]),
                                        style=common_style  # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_helicasa,
                                        language="python",
                                    ),
                                ),
                            ),
                            rx.accordion.item(
                                header="Topoisomerasa",
                                content=rx.box(
                                    rx.markdown(State.text["topoisomerasa_info"]),
                                    rx.heading("Ejemplo (se indica tras actuar la heliciasa)", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["topoisomerasa_action"]),
                                        style=common_style  # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_topoisomerasa,
                                        language="python",
                                    ),
                                ),
                            ),
                            rx.accordion.item(
                                header="SSB",
                                content=rx.box(
                                    rx.markdown(State.text["ssb_info"]),
                                    rx.heading("Ejemplo", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["ssb_action"]),
                                        style=common_style  # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_ssb,
                                        language="python",
                                    ),
                                ),
                            ),
                            variant = "surface",
                            collapsible=True,
                            width="100%",
                        )
                    ),
                    rx.divider(),
                    rx.section(
                        rx.heading("Fase de elongación", size="5"),
                        rx.markdown(State.text["fase_elongación"]),
                        rx.accordion.root(
                            rx.accordion.item(
                                header="Primasa",
                                content=rx.box(
                                    rx.markdown(State.text["primasa_info"]),
                                    rx.section(
                                        rx.heading("Ejemplo cadena líder", size="3"),
                                        rx.box(
                                            rx.markdown(State.text["primasa_action_1"]),
                                            style=common_style  # Cambia el color de fondo aquí
                                        ),
                                        rx.heading("Código", size="3"),
                                        rx.code_block(
                                            code_primasa_leader,
                                            language="python",
                                        ),
                                    ),
                                    rx.divider(),
                                    rx.section(
                                        rx.heading("Ejemplo cadena rezagada", size="3"),
                                        rx.box(
                                            rx.markdown(State.text["primasa_action_2"]),
                                            style=common_style  # Cambia el color de fondo aquí
                                        ),
                                        rx.heading("Código", size="3"),
                                        rx.code_block(
                                            code_primasa_lagger,
                                            language="python",
                                        ),
                                    ),
                                ),
                            ),
                            rx.accordion.item(
                                header="Cebador",
                                content=rx.box(
                                    rx.markdown(State.text["cebador_info"]),
                                ),
                            ),
                            rx.accordion.item(
                                header="ADN polimerasa III",
                                content=rx.box(
                                    rx.markdown(State.text["adn_polimerasa_III_info"]),
                                    rx.divider(),
                                    rx.section(
                                    rx.heading("Líder", size="3"),	
                                    rx.markdown(State.text["adn_polimerasa_III_leader"]),
                                    rx.heading("Ejemplo", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["adn_polimerasa_III_leader_action"]),
                                        style=common_style  # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_adn_polimerasa_III_leader,
                                        language="python",
                                    )),
                                    rx.divider(),
                                    rx.section(
                                    rx.heading("Rezagado", size="3"),
                                    rx.markdown(State.text["adn_polimerasa_III_lagger"]),
                                    rx.heading("Ejemplo", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["adn_polimerasa_III_laggard_action"]),
                                        style=common_style # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_adn_polimersa_rezagado,
                                        language="python",
                                    )),
                                ),
                            ),
                            variant = "surface",
                            collapsible=True,
                            width="100%",
                        )
                    ),
                    rx.divider(),
                    rx.section(
                        rx.heading("Fase de terminación", size="5"),
                        rx.markdown(State.text["fase_terminación"]),
                        rx.accordion.root(
                            rx.accordion.item(
                                header="ADN polimerasa I",
                                content=rx.box(
                                    rx.markdown(State.text["adn_polimerasa_I_info"]),
                                    rx.heading("Ejemplo", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["adn_polimerasa_I_action"]),
                                        style=common_style # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_replace_primers_with_dna,
                                        language="python",
                                    ),
                                ),
                            ),
                            rx.accordion.item(
                                header="Ligasa",
                                content=rx.box(
                                    rx.markdown(State.text["ligasa_info"]),
                                    rx.heading("Ejemplo", size="3"),
                                    rx.box(
                                        rx.markdown(State.text["ligase_action"]),
                                        style=common_style  # Cambia el color de fondo aquí
                                    ),
                                    rx.divider(),
                                    rx.heading("Código", size="3"),
                                    rx.code_block(
                                        code_ligase_action,
                                        language="python",
                                    ),
                                ),
                            ),
                            collapsible=True,
                            variant="surface",
                            width="100%",
                        )
                    ),
                    rx.section(
                        rx.heading("Esquema general código replicación:", size="5"),
                        rx.code_block(
                            code_replication,
                            language="python",
                        ),
                        rx.section(
                            rx.heading("Función replicación hebra líder", size="3"),
                            rx.code_block(
                                code_replication_leader,
                                language="python",
                            ),
                        ),
                        rx.section(
                            rx.heading("Función replicación hebra rezagada", size="3"),
                            rx.code_block(
                                code_replication_lagger,
                                language="python",
                            ),
                        ),
                    ),
                ),
                rx.text("No se ha subido ningún archivo."),
            ),
        ),
    )