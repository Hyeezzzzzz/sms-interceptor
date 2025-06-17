
# Guia de Instalação - SMS Interceptor CLI

Este guia irá ajudá-lo a configurar e instalar o SMS Interceptor CLI em seu sistema.

## Requisitos

Certifique-se de ter os seguintes softwares instalados em seu sistema:

*   **Python 3.10+**: Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
*   **Git**: Para clonar o repositório do projeto. Você pode baixá-lo em [git-scm.com](https://git-scm.com/downloads).

## Passos de Instalação

### Passo 1: Clonar o Repositório

Abra seu terminal ou prompt de comando e execute os seguintes comandos para clonar o projeto e navegar até o diretório:

```bash
git clone <URL_DO_REPOSITORIO> # Substitua <URL_DO_REPOSITORIO> pelo link real do repositório
cd sms-interceptor-cli
```

### Passo 2: Criar um Ambiente Virtual (Recomendado)

É altamente recomendável criar um ambiente virtual para isolar as dependências do projeto do seu ambiente Python global. Isso evita conflitos de pacotes.

```bash
python -m venv venv
```

**Ativar o Ambiente Virtual:**

*   **No Windows:**

    ```bash
    .\venv\Scripts\activate
    ```

*   **No Linux/macOS:**

    ```bash
    source venv/bin/activate
    ```

### Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Passo 4: Verificação

Para verificar se a instalação foi bem-sucedida e se a ferramenta está funcionando corretamente, execute o comando de ajuda:

```bash
python main.py --help
```

Se você vir a mensagem de ajuda do `sms-interceptor-cli`, a instalação foi concluída com sucesso!


