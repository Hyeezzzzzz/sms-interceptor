import argparse
from rich.console import Console
from rich.table import Table
import importlib
import os

console = Console()

def load_providers():
    providers = {}
    providers_dir = os.path.join(os.path.dirname(__file__), "providers")
    for filename in os.listdir(providers_dir):
        if filename.endswith(".py") and filename not in ["__init__.py", "base_provider.py"]:
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"providers.{module_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, module.BaseProvider) and attr is not module.BaseProvider:
                        provider_instance = attr()
                        providers[module_name.replace("_", "-")] = provider_instance
            except Exception as e:
                console.print(f"[red]Erro ao carregar o provedor {module_name}: {e}[/red]")
    return providers

def main():
    parser = argparse.ArgumentParser(
        description="SMS Interceptor CLI: Intercepte códigos SMS de números temporários."
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando: list-providers
    list_providers_parser = subparsers.add_parser(
        "list-providers", help="Lista os provedores de SMS disponíveis."
    )

    # Comando: list-numbers
    list_numbers_parser = subparsers.add_parser(
        "list-numbers", help="Lista os números de telefone disponíveis para um provedor."
    )
    list_numbers_parser.add_argument(
        "--provider",
        required=True,
        help="Nome do provedor (ex: receive-smss-com)"
    )

    # Comando: watch
    watch_parser = subparsers.add_parser(
        "watch", help="Monitora um número de telefone para novas mensagens."
    )
    watch_parser.add_argument(
        "--provider",
        required=True,
        help="Nome do provedor (ex: receive-smss-com)"
    )
    watch_parser.add_argument(
        "--number",
        required=True,
        help="Número de telefone a ser monitorado (ex: +1234567890)"
    )
    watch_parser.add_argument(
        "--sender",
        help="Remetente opcional para filtrar mensagens (ex: Google)"
    )

    args = parser.parse_args()

    providers = load_providers()

    if args.command == "list-providers":
        table = Table(title="Provedores de SMS Disponíveis")
        table.add_column("Nome do Provedor", style="cyan", no_wrap=True)
        table.add_column("URL Base", style="magenta")
        for name, provider in providers.items():
            table.add_row(name, provider.url)
        console.print(table)

    elif args.command == "list-numbers":
        provider_name = args.provider.replace("-", "_")
        if provider_name in providers:
            provider = providers[provider_name]
            console.print(f"[green]Buscando números para {args.provider}...[/green]")
            numbers = provider.get_numbers()
            if numbers:
                table = Table(title=f"Números Disponíveis para {args.provider}")
                table.add_column("Número", style="cyan", no_wrap=True)
                table.add_column("País", style="magenta")
                for num_info in numbers:
                    table.add_row(num_info["number"], num_info["country"])
                console.print(table)
            else:
                console.print(f"[yellow]Nenhum número encontrado para {args.provider}.[/yellow]")
        else:
            console.print(f"[red]Provedor \'{args.provider}\' não encontrado.[/red]")

    elif args.command == "watch":
        provider_name = args.provider.replace("-", "_")
        if provider_name in providers:
            provider = providers[provider_name]
            provider.watch_messages(args.number, args.sender)
        else:
            console.print(f"[red]Provedor \'{args.provider}\' não encontrado.[/red]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()


