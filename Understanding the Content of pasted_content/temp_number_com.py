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

class TempNumberComProvider(BaseProvider):
    def __init__(self):
        super().__init__("https://temp-number.com/")

    def get_numbers(self):
        numbers = []
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all country links
            country_links = soup.find_all('a', class_='country-box')
            
            for link in country_links:
                country_name = link.find('h4').get_text(strip=True)
                country_url = link['href']
                
                # Navigate to each country page to get numbers
                country_response = requests.get(country_url)
                country_response.raise_for_status()
                country_soup = BeautifulSoup(country_response.text, 'html.parser')
                
                number_items = country_soup.find_all('div', class_='number-box')
                for item in number_items:
                    number_tag = item.find('h4')
                    if number_tag:
                        number = number_tag.get_text(strip=True)
                        numbers.append({'number': number, 'country': country_name})
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Erro ao acessar {self.url}: {e}[/red]")
        return numbers

    def watch_messages(self, number, sender=None):
        console.print(f"[yellow]Monitorando o número [bold]{number}[/bold] em {self.url}...[/yellow]")
        
        # Construct the URL for the specific number
        # This might need adjustment based on how temp-number.com structures their number pages
        number_url = f"{self.url}number/{number.replace(\'+\', \'\')}" # Example, needs verification
        
        last_message_text = ""

        with Live(Spinner("dots", text=Text("Aguardando novas mensagens...", style="green")), refresh_per_second=4, console=console) as live:
            while True:
                try:
                    response = requests.get(number_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find messages - this part will be highly specific to temp-number.com's HTML structure
                    # This is a placeholder and needs to be adapted after inspecting the site
                    messages_container = soup.find('div', class_='messages-container') # Placeholder
                    if messages_container:
                        messages = messages_container.find_all('div', class_='message-item') # Placeholder
                        if messages:
                            latest_message = messages[0] # Assuming the latest message is the first one
                            message_text_tag = latest_message.find('p', class_='message-text') # Placeholder
                            message_sender_tag = latest_message.find('span', class_='message-sender') # Placeholder
                            message_time_tag = latest_message.find('span', class_='message-time') # Placeholder

                            if message_text_tag and message_sender_tag and message_time_tag:
                                current_message_text = message_text_tag.get_text(strip=True)
                                current_message_sender = message_sender_tag.get_text(strip=True)
                                current_message_time = message_time_tag.get_text(strip=True)

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


