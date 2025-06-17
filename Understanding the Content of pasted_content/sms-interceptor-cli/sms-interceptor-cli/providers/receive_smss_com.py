import requests
from bs4 import BeautifulSoup
import re
from .base_provider import BaseProvider
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
import time

console = Console()

class ReceiveSmssComProvider(BaseProvider):
    def __init__(self):
        super().__init__("https://receive-smss.com/")

    def get_numbers(self):
        numbers = []
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all elements that contain phone numbers and countries
            # The structure seems to be a div with class 'number-boxes-item'
            number_items = soup.find_all('div', class_='number-boxes-item')
            
            for item in number_items:
                number_tag = item.find('a', class_='number-a')
                country_tag = item.find('p', class_='number-country')
                
                if number_tag and country_tag:
                    number = number_tag.get_text(strip=True)
                    country = country_tag.get_text(strip=True)
                    numbers.append({'number': number, 'country': country})
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Erro ao acessar {self.url}: {e}[/red]")
        return numbers

    def watch_messages(self, number, sender=None):
        console.print(f"[yellow]Monitorando o número [bold]{number}[/bold] em {self.url}...[/yellow]")
        
        # Navigate to the specific number's page
        number_url = f"{self.url}number/{number.replace('+', '')}"
        
        last_message_text = ""

        with Live(Spinner("dots", text=Text("Aguardando novas mensagens...", style="green")), refresh_per_second=4, console=console) as live:
            while True:
                try:
                    response = requests.get(number_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find the messages container
                    messages_container = soup.find('div', class_='list-item-messages')
                    if messages_container:
                        messages = messages_container.find_all('div', class_='list-item')
                        if messages:
                            latest_message = messages[0] # Assuming the latest message is the first one
                            message_text_tag = latest_message.find('div', class_='list-item-message')
                            message_sender_tag = latest_message.find('div', class_='list-item-from')
                            message_time_tag = latest_message.find('div', class_='list-item-time')

                            if message_text_tag and message_sender_tag and message_time_tag:
                                current_message_text = message_text_tag.get_text(strip=True)
                                current_message_sender = message_sender_tag.get_text(strip=True)
                                current_message_time = message_time_time.get_text(strip=True)

                                if current_message_text != last_message_text:
                                    if sender is None or sender.lower() in current_message_sender.lower():
                                        live.stop()
                                        console.print(f"\n[bold blue]Nova Mensagem Recebida![/bold blue]")
                                        console.print(f"  [cyan]Remetente:[/cyan] {current_message_sender}")
                                        console.print(f"  [cyan]Hora:[/cyan] {current_message_time}")
                                        console.print(f"  [cyan]Mensagem:[/cyan] {current_message_text}")

                                        # Extract potential codes (5 to 8 digits)
                                        codes = re.findall(r'\b\d{5,8}\b', current_message_text)
                                        for code in codes:
                                            console.print(f"  [magenta]Possível Código Encontrado:[/magenta] [bold]{code}[/bold]")
                                        last_message_text = current_message_text
                                        live.start()
                        else:
                            live.text = Text("Aguardando novas mensagens... Nenhuma mensagem encontrada ainda.", style="green")
                    else:
                        live.text = Text("Aguardando novas mensagens... Container de mensagens não encontrado.", style="green")

                except requests.exceptions.RequestException as e:
                    live.stop()
                    console.print(f"[red]Erro ao acessar {number_url}: {e}[/red]")
                    live.start()
                except Exception as e:
                    live.stop()
                    console.print(f"[red]Ocorreu um erro inesperado: {e}[/red]")
                    live.start()

                time.sleep(10)


