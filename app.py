import streamlit as st    
import os  
import shutil   
import json  
from pathlib import Path

# Função para carregar as contas de anúncio a partir do arquivo JSON 
def carregar_contas_anuncio(): 
    ad_accounts_path = Path("criacao/ad_accounts/ad_accounts.txt") 
    with open(ad_accounts_path, 'r', encoding='utf-8') as f: 
        ad_accounts = json.load(f)
    return ad_accounts

# Função para carregar os interesses a partir do arquivo JSON
def carregar_interesses():
    interesses_path = Path("criacao/interesses/interests_corrigido.json")
    with open(interesses_path, 'r', encoding='utf-8') as f:
        interesses = json.load(f)["data"]
    return interesses

def carregar_publicos_personalizados():
    publicos_path = Path("criacao/publicos_personalizados/custom_audiences.json")
    with open(publicos_path, 'r', encoding='utf-8') as f:
        publicos = json.load(f)["data"]
    return publicos

def carregar_contas_facebook_instagram():
    contas_path = Path("criacao/contas_facebook_e_instagram/contas_facebook_e_instagram.json")
    with open(contas_path, 'r', encoding='utf-8') as f:
        contas = json.load(f)
    facebook_pages = contas.get("facebook_pages", {}).get("data", [])
    instagram_accounts = contas.get("instagram_accounts", {}).get("data", [])
    return facebook_pages, instagram_accounts


# Função para salvar as informações para cada anúncio
def salvar_informacoes_para_anuncio(base_path, anuncio_num, titulo, copy, descricao, link, arquivo_midia, facebook_page_id, instagram_account_id):
    anuncio_path = base_path / f'anuncios/anuncio_{anuncio_num}'
    anuncio_path.mkdir(parents=True, exist_ok=True)

    with open(anuncio_path / 'titulo/titulo.txt', 'w', encoding='utf-8') as f:
        f.write(titulo)
    
    with open(anuncio_path / 'copy/copy.txt', 'w', encoding='utf-8') as f:
        f.write(copy)
    
    with open(anuncio_path / 'descricao/descricao.txt', 'w', encoding='utf-8') as f:
        f.write(descricao)
    
    with open(anuncio_path / 'link/link_site.txt', 'w', encoding='utf-8') as f:
        f.write(link)
    
    if arquivo_midia is not None:
        if arquivo_midia.type.startswith('image'):
            foto_path = anuncio_path / 'photo'
            if foto_path.exists() and foto_path.is_dir():
                shutil.rmtree(foto_path)
            foto_path.mkdir(parents=True, exist_ok=True)
            with open(foto_path / arquivo_midia.name, 'wb') as f:
                f.write(arquivo_midia.getbuffer())
        elif arquivo_midia.type.startswith('video'):
            video_path = anuncio_path / 'video'
            video_path.mkdir(parents=True, exist_ok=True)
            with open(video_path / 'video.mp4', 'wb') as f:
                f.write(arquivo_midia.getbuffer())
    
    # Salvar a página do Facebook e a conta do Instagram selecionadas
    with open(anuncio_path / 'facebook_page/facebook_page.txt', 'w', encoding='utf-8') as f:
        f.write(facebook_page_id)
    
    with open(anuncio_path / 'instagram_account/instagram_account.txt', 'w', encoding='utf-8') as f:
        f.write(instagram_account_id)


# Função para salvar as informações para a conta de anúncio
def salvar_informacoes_para_conta(orçamento, quantidade_de_conjuntos, quantidade_de_anuncios, titulo_copy_descricao_link_midia_facebook_instagram, idade_min, idade_max, genero, conta_anuncio, interesses_selecionados, publicos_personalizados_selecionados, publicos_excluidos_selecionados):
    base_path = Path("criacao/informacoes")
    base_path.mkdir(parents=True, exist_ok=True)

    # Salvar a conta de anúncio selecionada 
    with open(base_path / 'ad_account/ad_account.txt', 'w', encoding='utf-8') as f: 
        f.write(conta_anuncio)

    # Processar o valor do orçamento
    orcamento_str = str(orçamento * 10)  # Multiplica por 10
    orcamento_str = orcamento_str.replace('.', '').replace(',', '')  # Remove ponto ou vírgula
    
    with open(base_path / 'orcamento/orcamento_ads.txt', 'w', encoding='utf-8') as f:
        f.write(orcamento_str)

    with open(base_path / 'quantidade_de_conjuntos/quantidade.txt', 'w', encoding='utf-8') as f:
        f.write(str(quantidade_de_conjuntos))

    # Salvar quantidade de anúncios
    with open(base_path / 'quantidade_de_anuncios/quantidade.txt', 'w', encoding='utf-8') as f:
        f.write(str(quantidade_de_anuncios))

    # Salvar as informações para cada anúncio
    for i in range(quantidade_de_anuncios):
        titulo, copy, descricao, link, arquivo_midia, facebook_page_id, instagram_account_id = titulo_copy_descricao_link_midia_facebook_instagram[i]
        salvar_informacoes_para_anuncio(base_path, i+1, titulo, copy, descricao, link, arquivo_midia, facebook_page_id, instagram_account_id)

    # Salvar idade mínima e máxima
    with open(base_path / 'age/age_min/age_min.txt', 'w', encoding='utf-8') as f: 
        f.write(str(idade_min)) 
    with open(base_path / 'age/age_max/age_max.txt', 'w', encoding='utf-8') as f:
        f.write(str(idade_max))

    # Salvar gênero masculino e feminino em arquivos separados
    male_path = base_path / 'gender/male/male.txt'
    female_path = base_path / 'gender/female/female.txt'
    
    if '1' in genero:
        male_path.parent.mkdir(parents=True, exist_ok=True)
        with open(male_path, 'w', encoding='utf-8') as f:
            f.write('1')
    else:
        if male_path.exists():
            with open(male_path, 'w', encoding='utf-8') as f:
                f.write('')

    if '2' in genero:
        female_path.parent.mkdir(parents=True, exist_ok=True)
        with open(female_path, 'w', encoding='utf-8') as f:
            f.write('2')
    else:
        if female_path.exists():
            with open(female_path, 'w', encoding='utf-8') as f:
                f.write('')

    # Salvar interesses selecionados
    interesses_path = base_path / 'interesses/interesses.txt'
    with open(interesses_path, 'w', encoding='utf-8') as f: 
        interesses_str = ", ".join([json.dumps({"id": interesse['id'], "name": interesse['name']}) for interesse in interesses_selecionados]) 
        f.write(interesses_str) 

    # Salvar públicos personalizados selecionados
    publicos_adicionados_path = base_path / 'publicos_personalizados/publicos_adicionados/publicos_personalizados.txt'
    publicos_adicionados_path.parent.mkdir(parents=True, exist_ok=True)
    with open(publicos_adicionados_path, 'w', encoding='utf-8') as f:
        publicos_adicionados_str = ", ".join([json.dumps({"id": publico['id'], "name": publico['name']}) for publico in publicos_personalizados_selecionados])
        f.write(publicos_adicionados_str)
    
    # Salvar públicos excluídos selecionados
    publicos_excluidos_path = base_path / 'publicos_personalizados/publicos_excluidos/publicos_excluidos.txt'
    publicos_excluidos_path.parent.mkdir(parents=True, exist_ok=True)
    with open(publicos_excluidos_path, 'w', encoding='utf-8') as f:
        publicos_excluidos_str = ", ".join([json.dumps({"id": publico['id'], "name": publico['name']}) for publico in publicos_excluidos_selecionados])
        f.write(publicos_excluidos_str)


    
# Função para executar o script da campanha
def executar_campanha(tipo_campanha, arquivo_midia):
    if tipo_campanha == "ABO":
        if arquivo_midia.type.startswith('image'):
            os.system("python criacao/purchase_campaign.py")
        elif arquivo_midia.type.startswith('video'):
            os.system("python criacao/purchase_campaign_video.py")
    elif tipo_campanha == "CBO":
        if arquivo_midia.type.startswith('image'):
            os.system("python criacao/purchase_campaign_CBO.py")
        elif arquivo_midia.type.startswith('video'):
            os.system("python criacao/purchase_campaign_video_CBO.py")

# Título da interface
st.title('Criação de Campanha')

# Carregar as contas de anúncio
ad_accounts = carregar_contas_anuncio() 
ad_account_options = {f"{account['name']} ({account['id'][4:]})": account['id'] for account in ad_accounts} 
 
# Campo de seleção para conta de anúncio
contas_anuncio_selecionadas = st.multiselect('Selecione as Contas de Anúncio', list(ad_account_options.keys()))

# Campo para selecionar o tipo de campanha (ABO ou CBO)
tipo_campanha = st.radio('Selecione o Tipo de Campanha', ['ABO', 'CBO'])

# Campos de entrada do usuário
orcamento = st.number_input('Orçamento diário', min_value=0.0, step=0.01, format="%.2f")

# Campo para determinar a quantidade de conjuntos de anúncios que serão criados
quantidade_de_conjuntos = st.number_input('Quantidade de conjuntos', min_value=1, max_value=50, value=1)

# Campo de seleção para idade
col1, col2 = st.columns(2)
with col1:
    idade_min = st.number_input('Idade Mínima', min_value=18, max_value=65, value=18)
with col2:
    idade_max = st.number_input('Idade Máxima', min_value=19, max_value=65, value=65)

# Campo de seleção para gênero
genero_opcoes = st.multiselect('Gênero', ['Masculino', 'Feminino'], default=['Masculino', 'Feminino'])
genero = [] 
if 'Masculino' in genero_opcoes: 
    genero.append('1') 
if 'Feminino' in genero_opcoes:
    genero.append('2')



# Carregar os públicos personalizados
publicos_personalizados = carregar_publicos_personalizados()

col1, col2 = st.columns(2)
with col1:
    # Campo de seleção para públicos personalizados
    publicos_personalizados_selecionados_nomes = st.multiselect('Selecione os Públicos Personalizados', [publico['name'] for publico in publicos_personalizados])
    # Mapear os nomes selecionados para os respectivos objetos de público
    publicos_personalizados_selecionados = [publico for publico in publicos_personalizados if publico['name'] in publicos_personalizados_selecionados_nomes]
with col2:
    # Campo de seleção para públicos a serem excluídos
    publicos_excluidos_nomes = st.multiselect('Selecione os Públicos a Excluir', [publico['name'] for publico in publicos_personalizados])
    # Mapear os nomes selecionados para os respectivos objetos de público
    publicos_excluidos_selecionados = [publico for publico in publicos_personalizados if publico['name'] in publicos_excluidos_nomes]




# Carregar os interesses
interesses = carregar_interesses()

# Campo de seleção para interesses
interesses_selecionados_nomes = st.multiselect('Selecione os Interesses', [interesse['name'] for interesse in interesses])

# Mapear os nomes selecionados para os respectivos objetos de interesse
interesses_selecionados = [interesse for interesse in interesses if interesse['name'] in interesses_selecionados_nomes]

# Carregar as contas do Facebook e Instagram
facebook_pages, instagram_accounts = carregar_contas_facebook_instagram()

# Campo para selecionar a quantidade de anúncios que serão criados
quantidade_de_anuncios = st.number_input('Quantidade de anúncios', min_value=1, max_value=5, value=1)

titulo_copy_descricao_link_midia_facebook_instagram = []
for i in range(quantidade_de_anuncios):
    # Usar markdown para criar o contêiner com fundo diferenciado
    st.markdown(
        f"""
        <style>
        .container {{
            background-color: #09090a;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        </style>
        <div class="container">
        """, unsafe_allow_html=True
    )
    
    st.subheader(f'Anúncio {i+1}')
    
    # Usar colunas para colocar os campos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        # Campo de seleção para a página do Facebook
        facebook_page_options = {page['name']: page['id'] for page in facebook_pages}
        facebook_page_selecionada = st.selectbox(f'Selecione a Página do Facebook para o Anúncio {i+1}', list(facebook_page_options.keys()))
        facebook_page_id = facebook_page_options[facebook_page_selecionada]
    
    with col2:
        # Campo de seleção para a conta do Instagram
        instagram_account_options = {account['username']: account['id'] for account in instagram_accounts}
        instagram_account_selecionada = st.selectbox(f'Selecione a Conta do Instagram para o Anúncio {i+1}', list(instagram_account_options.keys()))
        instagram_account_id = instagram_account_options[instagram_account_selecionada]

    titulo = st.text_input(f'Título (Headline) do Anúncio {i+1}')
    copy = st.text_area(f'Copy (Texto do anúncio) {i+1}')
    descricao = st.text_input(f'Descrição (Texto que fica abaixo do headline) {i+1}')
    link = st.text_input(f'Link do Anúncio {i+1}')
    arquivo_midia = st.file_uploader(f'Foto ou Vídeo do Anúncio {i+1}', type=['jpg', 'jpeg', 'png', 'mp4'])
    
    titulo_copy_descricao_link_midia_facebook_instagram.append((titulo, copy, descricao, link, arquivo_midia, facebook_page_id, instagram_account_id))
    
    st.markdown("</div>", unsafe_allow_html=True)


# Botão para salvar informações e criar campanhas
if st.button('Criar Campanha'):
    for conta_anuncio_selecionada in contas_anuncio_selecionadas:
        conta_anuncio = ad_account_options[conta_anuncio_selecionada]
        salvar_informacoes_para_conta(orcamento, quantidade_de_conjuntos, quantidade_de_anuncios, titulo_copy_descricao_link_midia_facebook_instagram, idade_min, idade_max, genero, conta_anuncio, interesses_selecionados, publicos_personalizados_selecionados, publicos_excluidos_selecionados)   
        st.success(f'Informações salvas com sucesso para a conta {conta_anuncio_selecionada}!')   
        executar_campanha(tipo_campanha, arquivo_midia)   
        st.success(f'Campanha criada com sucesso para a conta {conta_anuncio_selecionada}!')    



# streamlit run app.py