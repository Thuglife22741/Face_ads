from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from dotenv import load_dotenv
import glob
import json
import os

load_dotenv()

# Função para obter o único arquivo dentro de um diretório
def get_single_file_path(directory):
    files = glob.glob(os.path.join(directory, '*'))
    if len(files) == 1:
        return files[0]
    else:
        raise Exception(f"Esperava encontrar apenas um arquivo em {directory}, mas encontrei {len(files)} arquivos.")

# Função para ler o conteúdo de um arquivo
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Initialize the Facebook API with your credentials
access_token = os.getenv("my_access_token")
app_secret = os.getenv("my_app_secret")
app_id = os.getenv("my_app_id")
ad_account_id_file_path = get_single_file_path('criacao/informacoes/ad_account/')
ad_account_id = read_file(ad_account_id_file_path)

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)

def create_campaign(account_id):
    orcamento_file_path = get_single_file_path('criacao/informacoes/orcamento/')
    campaign = Campaign(parent_id=account_id)
    campaign.update({
        Campaign.Field.name: 'Campanha CBO criada de forma inteligente',
        Campaign.Field.status: Campaign.Status.active,
        Campaign.Field.objective: Campaign.Objective.outcome_sales,
        'special_ad_categories': [],  # Atualizado para um array vazio
        Campaign.Field.daily_budget: int(read_file(orcamento_file_path)),  # Defina o orçamento da campanha em centavos (10000 = R$ 100,00)
        Campaign.Field.bid_strategy: 'LOWEST_COST_WITHOUT_CAP'  # Estratégia de lances para CBO
    })
    campaign.remote_create(params={'status': Campaign.Status.active})
    return campaign

def create_ad_set(account_id, campaign_id, ad_set_name_suffix=""):
    # Obtenha o caminho do único arquivo no diretório
    age_min_file_path = get_single_file_path('criacao/informacoes/age/age_min/')
    age_max_file_path = get_single_file_path('criacao/informacoes/age/age_max/')
    gender_male_max_file_path = get_single_file_path('criacao/informacoes/gender/male')
    gender_female_max_file_path = get_single_file_path('criacao/informacoes/gender/female')
    interesses_file_path = get_single_file_path('criacao/informacoes/interesses/')
    publicos_personalizados_file_path = get_single_file_path('criacao/informacoes/publicos_personalizados/publicos_adicionados/')
    publicos_excluidos_file_path = get_single_file_path('criacao/informacoes/publicos_personalizados/publicos_excluidos/')

    # Filtra os gêneros para remover valores vazios
    genders = []
    male_gender = read_file(gender_male_max_file_path)
    female_gender = read_file(gender_female_max_file_path)
    
    if male_gender:
        genders.append(int(male_gender))  # Converte para inteiro
    if female_gender:
        genders.append(int(female_gender))  # Converte para inteiro

    # Ler os interesses como uma lista de dicionários
    interesses_str = read_file(interesses_file_path)
    interesses = json.loads(f"[{interesses_str}]")

    # Ler as audiências personalizadas e semelhantes a partir do arquivo
    publicos_personalizados_str = read_file(publicos_personalizados_file_path)
    custom_audiences = json.loads(f"[{publicos_personalizados_str}]")

    # Ler as audiências excluídas a partir do arquivo
    publicos_excluidos_str = read_file(publicos_excluidos_file_path)
    excluded_custom_audiences = json.loads(f"[{publicos_excluidos_str}]")

    ad_set = AdSet(parent_id=account_id)
    ad_set.update({
        AdSet.Field.name: f'Test Ad Set {ad_set_name_suffix}',  # Nome diferenciado para cada conjunto de anúncios
        AdSet.Field.campaign_id: campaign_id,
        AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
        AdSet.Field.optimization_goal: AdSet.OptimizationGoal.offsite_conversions,
        AdSet.Field.destination_type: AdSet.DestinationType.website,
        AdSet.Field.targeting: {
            'geo_locations': {'countries': ['BR']},
            'genders': genders,
            'age_min': int(read_file(age_min_file_path)),
            'age_max': int(read_file(age_max_file_path)),
            'publisher_platforms': ['facebook', 'instagram', 'audience_network', 'messenger'],
            'facebook_positions': ['feed', 'right_hand_column', 'instant_article', 'marketplace', 'video_feeds', 'story', 'search', 'facebook_reels'],
            'instagram_positions': ['stream', 'story', 'reels', 'explore'],
            'audience_network_positions': ['classic', 'instream_video', 'rewarded_video'],
            'device_platforms': ['mobile', 'desktop'],
            'interests': interesses,
            'custom_audiences': custom_audiences,  # Inclui as audiências personalizadas e semelhantes dinamicamente
            'excluded_custom_audiences': excluded_custom_audiences  # Inclui os públicos personalizados a serem excluídos
        },
        AdSet.Field.promoted_object: {
            'pixel_id': "1699722334166019",  # Adicionando o ID do Pixel diretamente
            'custom_event_type': 'PURCHASE'
        },
        AdSet.Field.status: AdSet.Status.active,
    })
    ad_set.remote_create(params={'status': AdSet.Status.active})
    return ad_set

def upload_image(account_id, image_path):
    image = AdImage(parent_id=account_id)
    image[AdImage.Field.filename] = image_path
    image.remote_create()
    return image[AdImage.Field.hash]

def create_ad_creative(account_id, image_path, ad_number):
    # Obtenha o caminho dos outros arquivos baseado no número do anúncio
    titulo_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/titulo/')
    copy_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/copy/')
    link_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/link/')
    descricao_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/descricao/')
    facebook_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/facebook_page/')
    instagram_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/instagram_account/')
    
    # Defina o mimetype com base na extensão do arquivo
    mimetype = 'image/png' if image_path.endswith('.png') else 'image/jpeg'

    creative = AdCreative(parent_id=account_id)
    creative.update({
        AdCreative.Field.name: f'Foto e copy gerada por Agentes GPT - Anúncio {ad_number}',
        AdCreative.Field.title: read_file(titulo_file_path),
        AdCreative.Field.body: read_file(copy_file_path),
        AdCreative.Field.object_story_spec: {
            'page_id': read_file(facebook_file_path),
            'instagram_user_id': read_file(instagram_file_path),
            'link_data': {
                'call_to_action': {'type': 'LEARN_MORE'},
                'image_hash': upload_image(account_id, image_path),
                'link': str(read_file(link_file_path)),
                'message': read_file(copy_file_path),
                'name': read_file(titulo_file_path),
                'description': read_file(descricao_file_path)
            },
            'image_data': {'filename': image_path, 'mimetype': mimetype} 
        },
        AdCreative.Field.degrees_of_freedom_spec: {
            'creative_features_spec': {
                'standard_enhancements': {
                    'enroll_status': 'OPT_IN'
                }
            }
        }
    })
    try:
        creative.remote_create()
    except Exception as e:
        print("Failed to create creative: ", str(e))
    return creative


def create_ad(account_id, ad_set_id, creative, ad_set_name_suffix=""):
    ad = Ad(parent_id=account_id)
    ad.update({
        Ad.Field.name: f'Test Ad {ad_set_name_suffix}',
        Ad.Field.adset_id: ad_set_id,
        Ad.Field.creative: {'creative_id': creative['id']},
        Ad.Field.status: Ad.Status.active,
    })
    try:
        ad.remote_create(params={'status': Ad.Status.active})
    except Exception as e:
        print("Failed to create ad: ", str(e))
    return ad

# Begin the ad creation process
campaign = create_campaign(ad_account_id)
image_path = get_single_file_path('criacao/informacoes/anuncios/anuncio_1/photo/')
image_hash = upload_image(ad_account_id, image_path)

# Iterar para criar múltiplos conjuntos de anúncios e anúncios
quantidade_de_conjuntos_file_path = get_single_file_path('criacao/informacoes/quantidade_de_conjuntos/')
quantidade_de_anuncios_file_path = get_single_file_path('criacao/informacoes/quantidade_de_anuncios/')

for i in range(int(read_file(quantidade_de_conjuntos_file_path))):  # Criando X conjuntos de anúncios dinamicamente
    ad_set = create_ad_set(ad_account_id, campaign['id'], ad_set_name_suffix=f"_{i+1}") 
    for j in range(1, int(read_file(quantidade_de_anuncios_file_path)) + 1):  # Criando Y anúncios por conjunto de anúncios 
        # Obtenha o caminho da mídia para o anúncio j
        image_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{j}/photo/')
        # Crie o anúncio com a mídia específica
        creative = create_ad_creative(ad_account_id, image_path, j) 
        ad = create_ad(ad_account_id, ad_set['id'], creative, ad_set_name_suffix=f"_{i+1}") 


print(f"Created Campaign ID: {campaign['id']}")
