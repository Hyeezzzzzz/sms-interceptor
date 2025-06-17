
# Manual de Uso - SMS Interceptor CLI

Este manual detalha como utilizar o SMS Interceptor CLI para listar provedores, números e monitorar mensagens SMS.

## Comandos Básicos

### Listando Provedores

O comando `list-providers` exibe uma tabela com todos os provedores de SMS temporários que a ferramenta suporta, juntamente com suas URLs base. Isso é útil para saber quais serviços você pode utilizar.

**Comando:**

```bash
python main.py list-providers
```

**Exemplo de Output:**

```
╭───────────────────────────────────┬───────────────────────────────────╮
│ Nome do Provedor                  │ URL Base                          │
├───────────────────────────────────┼───────────────────────────────────┤
│ receive-smss-com                  │ https://receive-smss.com/         │
│ smstome-com                       │ https://smstome.com/              │
│ temp-number-com                   │ https://temp-number.com/          │
╰───────────────────────────────────┴───────────────────────────────────╯
```

### Listando Números

Para ver os números de telefone disponíveis em um provedor específico, use o comando `list-numbers` e forneça o nome do provedor através do argumento `--provider`.

**Comando:**

```bash
python main.py list-numbers --provider receive-smss-com
```

**Exemplo de Output:**

```
╭───────────────────┬───────────────────╮
│ Número            │ País              │
├───────────────────┼───────────────────┤
│ +16143271062      │ United States     │
│ +19702584068      │ United States     │
│ ...               │ ...               │
╰───────────────────┴───────────────────╯
```

## Monitorando Mensagens

O comando `watch` é o coração da ferramenta, permitindo que você monitore um número de telefone específico em tempo real para novas mensagens. Você deve especificar o provedor e o número. Opcionalmente, pode filtrar as mensagens por remetente.

**Comando:**

```bash
python main.py watch --provider <nome_do_provedor> --number <numero_de_telefone> [--sender <remetente_opcional>]
```

*   `--provider`: O nome do provedor de SMS (ex: `receive-smss-com`).
*   `--number`: O número de telefone completo a ser monitorado (ex: `+1234567890`).
*   `--sender` (opcional): Um filtro para o remetente da mensagem. Apenas mensagens que contenham este texto no nome do remetente serão exibidas (ex: `Google`, `Discord`).

O script exibirá um spinner enquanto aguarda novas mensagens e, a cada 10 segundos, verificará se há atualizações. Quando uma nova mensagem for detectada, o spinner será pausado, a mensagem será exibida e o spinner será reiniciado.

**Exemplo 1 (Simples): Monitorar um número sem filtro de remetente.**

```bash
python main.py watch --provider receive-smss-com --number +16143271062
```

**Exemplo 2 (Avançado): Monitorar um número específico, de um provedor específico, buscando por uma mensagem do "Discord".**

```bash
python main.py watch --provider smstome-com --number +447911123456 --sender Discord
```

**Exemplo de Output de Mensagem:**

```

Nova Mensagem Recebida!
  Remetente: Discord
  Hora: 2 minutos atrás
  Mensagem: Seu código de verificação do Discord é: 123456. Não compartilhe este código.
  Possível Código Encontrado: 123456
```

## Adicionando um Novo Provedor (Para Desenvolvedores)

O SMS Interceptor CLI foi projetado para ser modular, facilitando a adição de novos provedores de SMS. Para adicionar um novo site, siga estes passos:

1.  Crie um novo arquivo Python dentro do diretório `providers/` (ex: `meu_novo_provedor.py`).
2.  Neste novo arquivo, crie uma classe que herde de `BaseProvider` (importada de `providers.base_provider`).
3.  Implemente os métodos `get_numbers()` e `watch_messages()` dentro da sua nova classe, adaptando a lógica de scraping para o HTML específico do novo site.

O sistema de carregamento de provedores do `main.py` detectará automaticamente sua nova classe e a tornará disponível para uso na CLI.


