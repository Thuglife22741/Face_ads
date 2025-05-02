# Solução para Gerenciamento de Anúncios do Facebook

Este projeto é uma aplicação Streamlit para gerenciar e criar campanhas de anúncios no Facebook e Instagram de forma automatizada.

## Funcionalidades

- Criação de campanhas de anúncios para Facebook e Instagram
- Seleção de contas de anúncio
- Configuração de orçamento diário
- Definição de públicos-alvo por idade, gênero e interesses
- Seleção de públicos personalizados
- Criação de múltiplos anúncios com diferentes conteúdos
- Suporte para campanhas ABO (Ad Set Budget Optimization) e CBO (Campaign Budget Optimization)
- Upload de imagens e vídeos para os anúncios

## Requisitos

- Python 3.7+
- Streamlit
- Facebook Marketing API

## Configuração

1. Clone o repositório:
```
git clone https://github.com/Thuglife22741/Face_ads.git
cd Face_ads
```

2. Crie e ative um ambiente virtual:
```
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Configure as credenciais do Facebook:
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   my_app_id="SEU_APP_ID"
   my_app_secret="SEU_APP_SECRET"
   my_access_token="SEU_ACCESS_TOKEN"
   ad_account_id="SUA_CONTA_DE_ANUNCIO"
   business_id="SEU_BUSINESS_ID"
   ```

## Uso

Execute a aplicação Streamlit:
```
streamlit run app.py
```

Acesse a interface no navegador através do endereço indicado no terminal (geralmente http://localhost:8501).

## Estrutura do Projeto

- `app.py`: Aplicação principal Streamlit
- `criacao/`: Scripts e dados para criação de campanhas
  - `ad_accounts/`: Informações sobre contas de anúncio
  - `contas_facebook_e_instagram/`: Dados de páginas do Facebook e contas do Instagram
  - `interesses/`: Dados sobre interesses para segmentação
  - `publicos_personalizados/`: Configurações de públicos personalizados
  - `purchase_campaign*.py`: Scripts para criação de diferentes tipos de campanhas

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.