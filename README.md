# Localizei

Localizei é uma aplicação web que ajuda os usuários a encontrar e gerenciar localizações usando códigos postais (CEP) no Brasil. Ela fornece uma interface intuitiva para buscar endereços, visualizá-los em um mapa e armazenar locais favoritos.

## Funcionalidades

- Registro e autenticação de usuários
- Busca de endereços usando CEP (Código de Endereçamento Postal brasileiro)
- Visualização interativa de mapa
- Gerenciamento de locais favoritos
- Design responsivo para diversos dispositivos

## Tecnologias Utilizadas

- Frontend:
  - HTML5
  - CSS3 (com estilos personalizados e Bootstrap)
  - JavaScript
  - Leaflet.js para integração de mapas
- Backend:
  - Python
  - Framework web Flask
- APIs:
  - ViaCEP para consulta de endereços

## Estrutura do Projeto

- `app/`: Diretório principal da aplicação
  - `templates/`: Templates HTML
  - `static/`: Recursos estáticos (CSS, JavaScript, imagens)
  - `auth/`: Arquivos relacionados à autenticação
  - `models/`: Modelos de banco de dados
- `config.py`: Configurações
- `run.py`: Ponto de entrada da aplicação

## Configuração e Instalação

1. Clone o repositório
2. Instale as dependências necessárias
3. Configure o banco de dados
4. Configure as variáveis de ambiente
5. Execute a aplicação

### Usando Docker

Alternativamente, você pode usar Docker para configurar e executar a aplicação:

1. Certifique-se de ter o Docker e o Docker Compose instalados em seu sistema
2. Na raiz do projeto, execute o seguinte comando:
   
   docker-compose up -d
   

## Uso

1. Registre uma nova conta ou faça login
2. Digite um CEP na barra de pesquisa para encontrar um endereço
3. Visualize a localização no mapa
4. Salve locais favoritos
5. Gerencie seu perfil e endereços salvos

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Gabriel Camargo
Email: gabriel.hc.contato@gmail.com
Telefone: (35) 98436-8617
