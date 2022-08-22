# Python-Ransomware-Detector-WIP

College yearly challenge (FIAP NEXT) by Bash Bunny. Heavy work in progress.

## 1. Funcionamento

### 1.1 Como o software funciona?

O detector de atividade de Ransomware funciona através de honeypots criados em diretórios específicos (e selecionados pelo usuário), os quais são monitorados pelo software, e ao detectar alguma modificação de escrita ou mudança de atributos destes honeypots, o software entende que é uma atividade de Ransomware, assim pegando o PID do processo do suposto Ransomware e finalizando-o.

### 1.2 Como são criados os honeypots?

Antes de qualquer coisa, é necessário entender a criação dos honeypots.
Estes são criados nos os diretórios passados pelo usuário, assim como os diretórios filhos destes.

Após a criação de todos os honeypots em todos os diretórios passados, é criado um arquivo .JSON com várias entradas, onde cada uma delas conterá o caminho absoluto do honeypot no sistema de arquivos e uma hash MD5 única para o honeypot em questão.

A hash MD5 única é gerada através dos bytes do arquivo de honeypot, o qual possui uma string única e aleatória gerada de 50 caracteres, a fim de evitar qualquer caso de hash duplicada.

Uma vez com o .JSON criado com sucesso, é criado um outro arquivo, o qual é simplesmente um arquivo .txt com uma lista que possui todos os nomes únicos de cada honeypot, uma vez que é possível gerar honeypots com nomes fixos (ex: honeypot-file.txt) ou nomes aleatórios (ex: e4tYj7Mna4Fpo.txt). Não será gerado mais do que um nome nesta lista caso a opção de "nomes aleatórios de honeypot" esteja desativada.

Durante todo esse processo de criação dos honeypots, ainda é utilizado o serviço de auditoria do Linux, que criará uma regra de monitoramento para honeypot gerado, assim fazendo com que cada honeypot que tenha sofrido uma modificação de escrita ou mudança de atributos seja logado para um arquivo de log do serviço de auditoria do Linux. Este log é crucial para realizar a finalização do processo do provável Ransomware.

Por fim, para o software funcionar, é necessário que ele seja executado como sudo, portanto, todos os arquivos de honeypot criados possuem apenas permissões de escrita pelo root (usuários comuns não conseguirão editar os honeypots).

### 1.3 Como é realizada a detecção e finalização de um provável processo malicoso?

Quando todas as etapas anteriores são finalizadas, os diretórios passados pelo usuário são monitadoros pelo Observer do module "watchdog" do Python, realizando a função de monitorar mudanças presentes nestes diretórios. No estágio atual do software, são apenas monitoradas mudanças em arquivos dentro destes diretórios (escrita ou mudança de atributos). Uma vez que um arquivo do diretório é modificado, ele retorna um output da ocorrência de um evento de modificação, o qual é tratado dentro do nosso software, para validar se a mudança em questão foi feita em um honeypot ou em um arquivo comum.

Caso o evento de modificação tenha sido realizado em um honeypot (que é monitado pelo Observer do watchdog e pelo próprio serviço de auditoria do Linux), será gerada uma hash MD5 com base nos bytes atual do arquivo, e, uma vez que esta hash MD5 atual seja diferente da hash MD5 salva no arquivo .JSON do honeypot modificado em questão, o software tratará esta atividade como sendo maliciosa, e então o software irá recorrer aos logs do serviço de auditoria do Linux, puxando o último log gerado (que será o log do honeypot modificado), e dentro deste log será possível pegar diversas informações valiosas, onde uma delas é justamente o PID do provável Ransomware.

Com o PID do provável Ransomware em mãos, o nosso software simplesmente executa uma chamada de sistema para matar o processo com o PID em questão.

Todo esse processo descrito acima (do início da detecção até a morto do processo) leva em média 0.244s (com base em 20 testes realizados com certas configurações definidas).

## 2. Configurações

### 1.1 Configurações disponíveis do Audit

- **path_to_audit (path):** caminho absoluto para a pasta do serviço de auditoria do Linux;
- **path_to_audit_config (path):** caminho absoluto da pasta de configurações do serviço de auditoria do Linux;
- **path_to_audit_custom_rule_file (path):** caminho absoluto para o arquivo com as regras de auditoria para cada honeypot;
- **audit_custom_rules_key (string):** string que definirá a key para os logs de modificação dos honeypots.

### 1.2 Configurações disponíveis do Gerador de Honeypot

- **directory_list (list):** lista de diretórios que serão gerados os honeypots;
- **honeypot_file_name (string):** nome fixo dos arquivos de honeypot (essa opção apenas é utilizada caso a opção "random_honeypot_file_name" esteja desativada);
- **path_to_config_folder (path):** caminho absoluto para a pasta de configurações do anti-ransomware;
- **json_file_name (string):** nome do arquivo .JSON que conterá as entradas de caminhos absolutos dos honeypots e as hashes MD5 únicas para cada honeypot;
- **honeypot_names_file (string):** nome do arquivo .txt que conterá todos os nomes únicos de cada honeypot gerado (caso a opção "random_honeypot_file_name" esteja desativa, será gerado apenas o nome definido no "honeypot_file_name");
- **audit_obj (object):** objeto do serviço de auditoria do Linux que foi configurado previamente;
- **honeypot_interval (int):** intervalo de criação dos honeypots. Basicamente, caso o valor seja definido como 5, será criado 1 honeypot a cada 5 diretórios filhos do diretório passado na "directory_list";
- **disable_honeypot_interval (bool):** função para desativar o intervalo de criação dos honeypots, portanto, será criado 1 honeypot a cada diretório filhos do diretório passado na "directory_list";
- **random_honeypot_file_name (bool):** função para gerar um nome aleatório e único para cada honeypot gerado (ex: eT5bM93UxAS8);
- **hidden_honeypot_file (bool):** função para definir se os honeypots serão arquivos ocultos ou não;
- **honeypot_file_extension (string):** função para definir qual será a extensão dos arquivos de honeypot (o valor padrão é .txt);
- **delete (bool):** função para definir se o software deve criar novos honeypots ou deletar os já existentes;

### 1.3 Configurações disponíveis do Monitor do Sistema de Arquivos

- **directory_list (list):** lista de diretórios que serão monitorados;
- **honeypot_file_name (string):** nome fixo dos arquivos de honeypot. Essa opção não é utilizada por padrão;
- **path_to_config_folder (path)**: caminho absoluto para a pasta de configurações do anti-ransomware;
- **json_file_name (string):** nome do arquivo .JSON que conterá as entradas de caminhos absolutos dos honeypots e as hashes MD5 únicas para cada honeypot;
- **honeypot_names_file (string):** nome do arquivo .txt que conterá todos os nomes únicos de cada honeypot gerado (caso a opção "random_honeypot_file_name" esteja desativa, será gerado apenas o nome definido no "honeypot_file_name");
- **audit_obj (object):** objeto do serviço de auditoria do Linux que foi configurado previamente;

## Tabela de performance

O Ransomware utilziado para teste é um Ransomware próprio e simples com o objetivo de ser o mais rápido possível, a fim de testar a performance do anti-Ransomware. Os testes foram realizados com o arquivo de log totalmente limpo.

### Configuração do sistema utilizado para teste

| Nome | Hardware |
| --- | --- |
| CPU |  AMD Ryzen 5 1600AF 3.20Ghz Stock |
| MOBO |  Gigabyte B450M DSH3 rev. 1.0 (F50 BIOS) |
| GPU |  ASUS Radeon RX 570 ROG Strix 4GB Stock |
| RAM |  2x8GB Corsair Vengeance LPX DDR4 2666Mhz |
| PSU |  Corsair CX600 |
| SSD |  Crucial BX500 240GB |
| HDD |  Seagate Barracuda 2TB |
| OS |  Windows 10 Pro 64 bi |
