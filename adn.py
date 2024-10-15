import random
from Bio import SeqIO
import time

class ADN:
    def __init__(self, adn):
        self.adn = adn
        self.pairs_adn_adn_comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
        self.pairs_adn_arn_comp = {"A": "U", "T": "A", "C": "G", "G": "C"}
        self.pairs_arn_adn = {"A": "A", "U": "T", "C": "C", "G": "G"}
        self.new_comp_chain_1 = []
        self.new_comp_chain_2 = []
        self.position_helicasa = 0
        self.replicated = False
        self.chain_1_processed = []
        self.chain_2_processed = []
        self.text = {}
        self.cebador_lider = []
        self.cebador_rezagado = []
        self.rezagado_cebador_positions = []
        self.n_fragmentos_okazaki = 0
        self.create_info()

    def create(self):
        self.chain_1 = []
        self.chain_2 = []

        for i in range(0, len(self.adn)):
            self.chain_1.append(self.adn[i])
            self.chain_2.append(self.get_complementary_base(self.pairs_adn_adn_comp, self.adn[i]))
            print(self.chain_1)

    def create_info(self):
        self.text["fase_iniciación"] = (
            "La replicación del ADN comienza en un punto concreto de la mólecula de ADN al encontrar una secuencia de nucleótidos llamada origen de replicación. Durante este proceso actúan los siguientes componentes:"
        )
        self.text["helicasa_info"] = (
            "Es una enzima que rompe los puentes de hidrógeno entre las bases nitrogenadas del ADN "
            "permitiendo que las dos cadenas se separen y se expongan para que la ADN polimerasa pueda usarlas "
            "como molde para la replicación. "
        )          
        self.text["topoisomerasa_info"] = (
            "Es una enzima que se encarga de eliminar las tensiones o superenrollamientos causados por la helicasa al separar las cadenas de ADN."
        )
        self.text["ssb_info"] = (
            "Son unas proteínas que mantienen las hebras separadas, impidiendo que se vuelvan a unir durante la replicación."
        )
        self.text["fase_elongación"] = (
            "Para que las enzimas ADN-polimerasas puedan comenzar a sintetizar las nuevas cadenas de ADN, necesitan los siguientes elementos:"
        )
        self.text["primasa_info"] = (
            "Es una ARN polimerasa encargada de sintetizar los cebadores."
        )

        self.text["cebador_info"] = (
            "Es un fragmento corto de ARN que se une a la cadena de ADN molde y sirve como punto de inicio para la síntesis de la nueva cadena de ADN. En la hebra líder solo se requiere un cebador, mientras que en la hebra rezagada se necesitan varios."
        )

        self.text["adn_polimerasa_III_info"] = (
            "Las enzimas ADN polimerasa III actúan de forma distinta dependiendo de la hebra sobre la que actúen. Lo que es común es que la energía necesaria para la síntesis es proporcionada por los propios nucleótidos, que pierden dos grupos fosfato."
        )

        self.text["adn_polimerasa_III_leader"] = (
            "En la hebra líder solo se necesita un cebador para comenzar a sintetizar los nucleótidos complementarios de forma continua (en sentido 5'-3')."
        )

        self.text["adn_polimerasa_III_lagger"] = (
            "La hebra rezagada se replica de forma discontinua en sentido 3'-5'. La ADN polimerasa III sintetiza fragmentos de Okazaki, que son pequeñas secuencias de nucleótidos separadas por cebadores."
        )

        self.text["fase_terminación"] = (
            "La ADN polimerasa III finaliza la síntesis de nuevos nucleótidos tras encontrar una secuencia de terminación. Los siguientes elementos se involucran en esta fase:"
        )

        self.text["adn_polimerasa_I_info"] = (
            "Es una enzima llamada exonucleasa que se encarga de sustituir los cebadores de ARN por ADN."
        )

        self.text["ligasa_info"] = (
            "Es una enzima que se encarga de unir los fragmentos de Okazaki."
        )


    def start_replication(self):
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
        replicated_leader, replicated_lagger = self.ligase_action()
        print("Hebra líder replicada: " + replicated_leader)
        print("Hebra rezagada replicada: " + replicated_lagger)

    def get_complementary_base(self, pairs, base):
        return pairs[base]

    def complement_generator(self, chain, origin="adn", target="adn"):
        complementary = []
        pairs = {}

        if origin == "adn" and target == "adn":
            pairs = self.pairs_adn_adn_comp
        elif origin == "adn" and target == "arn":
            pairs = self.pairs_adn_arn_comp

        for base in chain:
            complementary.append(self.get_complementary_base(pairs, base))

        return complementary

    def helicasa_action(self, i):
        self.chain_1_processed.append(self.chain_1[i])
        self.chain_2_processed.append(self.chain_2[i])

        self.position_helicasa = i

        chain_1_str = "".join(self.chain_1_processed)
        chain_2_str = "".join(self.chain_2_processed)

        text = f"Helicasa en posición: {self.position_helicasa + 1}\n\nHebra 1: {chain_1_str}\n\nHebra 2: {chain_2_str}\n\n"

        if i == 0:
            self.text["helicasa_action_1"] = text
        
        elif i == len(self.adn) - 1:
            text = f"Helicasa en posición: {self.position_helicasa + 1}\n\nHebra 1: {chain_1_str}\n\nHebra 2: {chain_2_str}\n\nLa helicasa ha terminado de actuar en la cadena de ADN."
            self.text["helicasa_action_2"] = text

        print(text)


    def topoisomerasa_action(self):
        """Simula la topoisomerasa."""
        text = f"La topoisomerasa ha comenzado a actuar para aliviar la tensión generada por la helicasa.\n\n"
        self.text["topoisomerasa_action"] = text

        print(text)

    def bind_ssb(self, position):
        """Simula la unión de proteínas SSB."""
        text = f"Proteínas SSB unidas a las posiciones {position - 2} a {position} en ambas hebras.\n\n"
        if self.position_helicasa == 2:
            self.text["ssb_action"] = text

        print(text)


    def replicate_lider(self):
        if self.position_helicasa < 10:
            self.activate_cebador_lider()
        else:
            self.adn_polimerasa_lider_action()

    def activate_cebador_lider(self):
        base_comp = self.get_complementary_base(self.pairs_adn_arn_comp ,self.chain_1_processed[self.position_helicasa - 1])
        self.cebador_lider.append(base_comp)
        self.new_comp_chain_1.append(base_comp)

        if self.position_helicasa == 1:
            text = f"La primasa líder en la posición {self.position_helicasa} ha comenzado a sintetizar el cebador: {base_comp}\n\nCebador líder: {''.join(self.cebador_lider)}\n\nRéplica complementaria líder: {''.join(self.new_comp_chain_1)}\n\n"
            self.text["primasa_action_1"] = text
        
        elif self.position_helicasa == 10:
            text = f"La primasa líder en la posición {self.position_helicasa} ha añadido al cebador: {base_comp}\n\nCebador líder: {''.join(self.cebador_lider)}\nRéplica complementaria líder: {''.join(self.new_comp_chain_1)}\n\nLa primasa ha sintetizado el cebador líder correctamente."
            self.text["primasa_action_2"] = text
        
        else:
            text = f"La primasa líder en la posición {self.position_helicasa} ha añadido al cebador: {base_comp}\n\nCebador líder: {''.join(self.cebador_lider)}\nRéplica complementaria líder: {''.join(self.new_comp_chain_1)}\n\n"
        
        print(text)

    def adn_polimerasa_lider_action(self):
        if len(self.new_comp_chain_1) < len(self.chain_1_processed) -1:
            base_comp = self.get_complementary_base(self.pairs_adn_adn_comp, self.chain_1_processed[self.position_helicasa - 1])
            self.new_comp_chain_1.append(base_comp)

            if self.position_helicasa == 10:
                text = f"La ADN polimerasa III líder ha encontrado el cebador y ha comenzado a replicar la cadena de ADN.\n\n ADN polimerasa líder en posición {self.position_helicasa} ha añadido la base: {base_comp}\n\nRéplica complementaria líder: {''.join(self.new_comp_chain_1)}\n\n"
                self.text["adn_polimerasa_III_leader_action"] = text
            else:
                text = f"ADN polimerasa líder en posición {self.position_helicasa} ha añadido la base: {base_comp}\n\nRéplica complementaria líder: {''.join(self.new_comp_chain_1)}\n\n"
        
        elif len(self.new_comp_chain_1) == len(self.chain_1_processed) - 1:
            base_comp = self.get_complementary_base(self.pairs_adn_adn_comp, self.chain_1_processed[self.position_helicasa])
            self.new_comp_chain_1.append(base_comp)
            text = f"ADN polimerasa III líder en posición {self.position_helicasa+1} ha añadido la base: {base_comp}\n\nRéplica complementaria líder: {''.join(self.new_comp_chain_1)}\n\nLa ADN polimerasa III líder ha terminado de replicar la cadena de ADN."
            self.text["adn_polimerasa_III_leader_action"] += text
        
        elif len(self.new_comp_chain_1) == len(self.chain_1_processed):
            text = f"La ADN polimerasa III líder ha terminado de replicar la cadena de ADN líder.\n\n"
            self.text["adn_polimerasa_III_leader_action"] += text
        
        print(text)


    def activate_cebador_rezagado(self):
        base_comp = self.get_complementary_base(self.pairs_adn_arn_comp, self.chain_2_processed[self.position_helicasa - 1])
        self.cebador_rezagado.append(base_comp)
        self.new_comp_chain_2.append(base_comp)
        self.rezagado_cebador_positions.append(self.position_helicasa - 1)
        text = f"Un cebador rezagado ha sido sintetizado por la primasa en la posición {self.position_helicasa}\n\nCebador rezagado: {''.join(self.cebador_rezagado)}\n\nRéplica complementaria rezagada: {''.join(self.new_comp_chain_2)}\n\n"

        if self.position_helicasa == 1:
            self.text["primasa_action"] = text
        
        print(text)
    
    def adn_polimerasa_rezagada_action(self):
        if len(self.new_comp_chain_2) < len(self.chain_2_processed) - 1:
            base_comp = self.get_complementary_base(
                self.pairs_adn_adn_comp, self.chain_2_processed[self.position_helicasa - 1]
            )
            self.new_comp_chain_2.append(base_comp)
            text = f"ADN polimerasa III rezagada en posición {self.position_helicasa} ha añadido la base: {base_comp} a un fragmento de okazaki.\n\nRéplica complementaria rezagada: {''.join(self.new_comp_chain_2)}\n\n"

            if self.position_helicasa == 2:
                self.text["adn_polimerasa_III_laggard_action"] = text
        
        elif len(self.new_comp_chain_2) == len(self.chain_2_processed) - 1:
            base_comp = self.get_complementary_base(
                self.pairs_adn_adn_comp, self.chain_2_processed[self.position_helicasa]
            )
            self.new_comp_chain_2.append(base_comp)
            text = f"ADN polimerasa III rezagada en posición {self.position_helicasa+1} ha añadido la base: {base_comp} a un fragmento de okazaki.\n\nRéplica complementaria rezagada: {''.join(self.new_comp_chain_2)}\n\n"
            self.text["adn_polimerasa_III_laggard_action"] += text
        
        elif len(self.new_comp_chain_2) == len(self.chain_2_processed):
            text = f"La ADN polimerasa III rezagada ha terminado de replicar la cadena de ADN rezagada.\n\nSe han sintetizado {self.n_fragmentos_okazaki} fragmentos de Okazaki."
            self.text["adn_polimerasa_III_laggard_action"] += text
            self.replicated = True
        
        print(text)


    def replicate_rezagada(self):
        if self.cebador_rezagado == []:
            self.activate_cebador_rezagado()
        else:
            self.adn_polimerasa_rezagada_action()
            if (self.position_helicasa - 1) - self.rezagado_cebador_positions[-1] == 3:
                self.cebador_rezagado = []
                self.n_fragmentos_okazaki += 1


    def replace_primers_with_dna(self):
        """Sustituye cebadores por ADN."""
        for i in range(len(self.cebador_lider)):
            base = self.cebador_lider[i]
            self.new_comp_chain_1[i] = self.pairs_arn_adn[base]

        for position in self.rezagado_cebador_positions:
            self.new_comp_chain_2[position] = self.get_complementary_base(
                self.pairs_arn_adn, self.new_comp_chain_2[position]
            )
        
        text = f"La ADN polimerasa I está sustituyendo los cebadores por ADN en ambas cadenas.\n\nCadena líder replicada tras sustituir los cebadores: {''.join(self.new_comp_chain_1)}\n\nCadena rezagada replicada tras sustituir los cebadores: {''.join(self.new_comp_chain_2)}\n\n"
        self.text["adn_polimerasa_I_action"] = text

        print(text)

    def ligase_action(self):
        """La ligasa une los fragmentos de Okazaki en la cadena rezagada."""

        # Implementación simulada: los fragmentos de Okazaki se unen
        # Los fragmentos ya fueron añadidos en la cadena rezagada (`new_comp_chain_2`), aquí solo indicamos la unión
        text = f"La ADN ligasa está uniendo los fragmentos de Okazaki en la hebra rezagada.Los fragmentos de Okazaki han sido unidos por la ADN ligasa."
        self.text["ligase_action"] = text

        print(text)

        return "".join(self.new_comp_chain_1), "".join(self.new_comp_chain_2)

    def validate_replication(self):
        """Valida si la replicación se ha realizado correctamente."""

        # Comprobar la longitud de las cadenas replicadas
        if len(self.chain_1) != len(self.new_comp_chain_2) or len(self.chain_2) != len(
            self.new_comp_chain_1
        ):

            print(
                "Error: Las longitudes de las cadenas replicadas no coinciden con las originales."
            )
            print("Hebra líder original: " + "".join(self.chain_1))
            print("Hebra que debería ser la líder: " + "".join(self.new_comp_chain_2))
            print("Hebra rezagada original: " + "".join(self.chain_2))
            print("Hebra que debería ser la rezagada: " + "".join(self.new_comp_chain_1))
            return

        # Validar la hebra líder
        correct_leader = self.chain_2 == self.new_comp_chain_1

        correct_lagging = self.chain_1 == self.new_comp_chain_2

        print(correct_leader)
        print(correct_lagging)

        if correct_leader and correct_lagging:
            print("La replicación se ha realizado correctamente.")
        else:
            print(
                "Error en la replicación. Las cadenas replicadas no coinciden con las originales."
            )

            print("Hebra líder original: " + "".join(self.chain_1))
            print("Hebra que debería ser la líder: " + "".join(self.new_comp_chain_2))
            print("Hebra rezagada original: " + "".join(self.chain_2))
            print("Hebra que debería ser la rezagada: " + "".join(self.new_comp_chain_1))

def chain_generator(n):
    return "".join([random.choice("ATCG") for i in range(n)])

def get_user_input_sequence():
    """Solicita al usuario que ingrese manualmente una secuencia de ADN."""
    input_sequence_size = input("Por favor, ingresa el tamaño de la secuencia de ADN: ")
    # Verifica que el usuario haya ingresado un número entero
    if input_sequence_size.isdigit() and int(input_sequence_size) >= 11:
        return chain_generator(int(input_sequence_size))
    else:
        print("Por favor, ingresa un número entero y mayor a 10.")
        return get_user_input_sequence()



def choose_input_method():
    """Permite al usuario elegir entre ingresar una secuencia manualmente o cargar un archivo FASTA."""
    choice = input(
        "¿Deseas generar una secuencia de ADN de forma aleatoria? (sí/no): "
    ).lower()

    if choice == "sí" or choice == "si":
        return get_user_input_sequence()
    elif choice == "no":
        archivo = input("Por favor, ingresa la ruta del archivo FASTA: ")
        return read_fasta_file(archivo)
    else:
        print("Opción no válida. Por favor, elige 'sí' o 'no'.")
        return choose_input_method()


def read_fasta_file(archivo_fasta):
    """Lee un archivo FASTA y devuelve la secuencia de nucleótidos."""
    with open(archivo_fasta, "r") as archivo:
        for record in SeqIO.parse(archivo, "fasta"):
            secuencia_adn = str(record.seq)
            print(f"Secuencia de ADN leída del archivo: {secuencia_adn}")
            return secuencia_adn



# Iniciar la replicación
secuencia_adn = choose_input_method()
ADN_1 = ADN(secuencia_adn)
ADN_1.create()
ADN_1.start_replication()
ADN_1.validate_replication()
