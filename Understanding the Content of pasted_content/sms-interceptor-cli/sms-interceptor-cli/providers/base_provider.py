from abc import ABC, abstractmethod

class BaseProvider(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_numbers(self):
        """
        Deve retornar uma lista de dicionários, onde cada dicionário representa um número de telefone
        e contém as chaves 'number' e 'country'.
        Ex: [{'number': '+1234567890', 'country': 'US'}]
        """
        pass

    @abstractmethod
    def watch_messages(self, number, sender=None):
        """
        Monitora as mensagens para um número específico.
        Deve imprimir as novas mensagens encontradas e possíveis códigos.
        """
        pass


