import reflex as rx
from .scripts.adn import chain_generator, read_fasta_file, ADN


class State(rx.State):
    """The app state."""

    file: str = ""
    file_uploaded: bool = False
    content: str = ""
    form_data: dict = {}
    file_output: str = ""
    text: dict = {}


    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of a single file.

        Args:
            files: The uploaded files.
        """
        if files:

            file = files[0]
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            self.file_uploaded = True
            self.file = file.filename
            
            self.content = read_fasta_file(outfile)
            await self.handle_replication()
            

    async def handle_generate_adn(self, form_data: dict):
        """Handle the generation of a random ADN sequence.

        Args:
            n: The length of the sequence.
        """
        self.file_uploaded = True
        self.form_data = form_data
        input = self.form_data["input"]
        if input.isdigit() and int(input) > 11:
            self.content = chain_generator(int(input))
            await self.handle_replication()
        else:    
            self.content = "Por favor, ingrese un número entero mayor a 11."

    async def handle_replication(self):
        """Handle the replication of the DNA sequence."""
        adn = ADN(self.content)
        adn.create()
        adn.start_replication()
        self.text = adn.text

        
        

        
    


    
        