from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo
from dotenv import load_dotenv
import json
import glob
import cv2
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
    campaign = Campaign(parent_id=account_id)
    campaign.update({
        Campaign.Field.name: 'Campanha ABO de vídeo criada por código',
        Campaign.Field.status: Campaign.Status.active,
        Campaign.Field.objective: Campaign.Objective.outcome_sales,
        'special_ad_categories': []  # Atualizado para um array vazio
    })
    campaign.remote_create(params={'status': Campaign.Status.active})
    return campaign

def create_ad_set(account_id, campaign_id, ad_set_name_suffix=""):
    # Obtenha o caminho do único arquivo no diretório
    orcamento_file_path = get_single_file_path('criacao/informacoes/orcamento/')
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
        AdSet.Field.name: f'Test Ad Set {ad_set_name_suffix}',  # Nome diferenciado para cada conjunto de anúncios,
        AdSet.Field.campaign_id: campaign_id,
        AdSet.Field.daily_budget: int(read_file(orcamento_file_path)),
        AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
        AdSet.Field.optimization_goal: AdSet.OptimizationGoal.offsite_conversions,
        AdSet.Field.bid_strategy: AdSet.BidStrategy.lowest_cost_without_cap,
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

def extract_frame_from_video(video_path, frame_time=0.5):
    # Use OpenCV para capturar um frame do vídeo
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Determine o número do frame a ser capturado (exemplo: 50% do comprimento do vídeo)
    frame_number = int(total_frames * frame_time)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Defina o caminho para salvar o frame na subpasta 'video_thumb/' dentro de 'video/'
        video_dir = os.path.dirname(os.path.dirname(video_path))  # Subir um nível para a pasta 'video/'
        thumb_dir = os.path.join(video_dir, 'video_thumb')
        os.makedirs(thumb_dir, exist_ok=True)  # Cria a pasta 'video_thumb' se ela não existir
        frame_image_path = os.path.join(thumb_dir, "thumbnail.jpg")
        
        # Salve o frame como um arquivo de imagem
        cv2.imwrite(frame_image_path, frame)
        return frame_image_path
    else:
        raise Exception("Failed to extract frame from video")


def upload_image(account_id, image_path):
    image = AdImage(parent_id=account_id)
    image[AdImage.Field.filename] = image_path
    image.remote_create()
    return image[AdImage.Field.hash]

def upload_video(account_id, video_path):
    video = AdVideo(parent_id=account_id)
    video[AdVideo.Field.filepath] = video_path
    video.remote_create()
    return video[AdVideo.Field.id]


image_path = get_single_file_path('criacao/informacoes/anuncios/anuncio_1/photo/')
image_hash = upload_image(ad_account_id, image_path)

def create_ad_creative(account_id, video_id, image_hash, ad_number):
    # Obtenha o caminho dos arquivos baseados no número do anúncio
    titulo_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/titulo/')
    copy_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/copy/')
    link_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/link/')
    description_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/descricao/')  # Adicionando o caminho para a descrição
    facebook_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/facebook_page/')
    instagram_file_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{ad_number}/instagram_account/')

    creative = AdCreative(parent_id=account_id)
    creative.update({
        AdCreative.Field.name: f'Vídeo e copy gerada por Agentes GPT - Anúncio {ad_number}',
        AdCreative.Field.title: read_file(titulo_file_path),
        AdCreative.Field.body: read_file(copy_file_path),
        AdCreative.Field.object_story_spec: {
            'page_id': read_file(facebook_file_path),
            'instagram_user_id': read_file(instagram_file_path),
            'video_data': {
                'call_to_action': {
                    'type': 'LEARN_MORE',
                    'value': {
                        'link': str(read_file(link_file_path))
                    }
                },
                'video_id': video_id,
                'image_hash': image_hash,  # Adicionando o hash da imagem aqui
                'message': read_file(copy_file_path),
                'title': read_file(titulo_file_path),
                'link_description': read_file(description_file_path),
            }
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


def create_ad(account_id, ad_set_id, creative):
    ad = Ad(parent_id=account_id)
    ad.update({
        Ad.Field.name: 'Test Ad',
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
video_path = 'criacao/informacoes/anuncios/anuncio_1/video/video_file/video.mp4'
video_id = upload_video(ad_account_id, video_path)

# Iterar para criar múltiplos conjuntos de anúncios e anúncios
quantidade_de_conjuntos_file_path = get_single_file_path('criacao/informacoes/quantidade_de_conjuntos/')
quantidade_de_anuncios_file_path = get_single_file_path('criacao/informacoes/quantidade_de_anuncios/')

# Exemplo de uso no loop
for i in range(int(read_file(quantidade_de_conjuntos_file_path))):  # Exemplo: criando X conjuntos de anúncios
    ad_set = create_ad_set(ad_account_id, campaign['id'], ad_set_name_suffix=f"_{i+1}")
    for j in range(1, int(read_file(quantidade_de_anuncios_file_path)) + 1):  # Criando Y anúncios por conjunto de anúncios 
        # Obtenha o caminho do vídeo para o anúncio j
        video_path = get_single_file_path(f'criacao/informacoes/anuncios/anuncio_{j}/video/video_file/')
        
        # Extrair um frame do vídeo e salvar como imagem
        frame_image_path = extract_frame_from_video(video_path)
        
        # Carregar a imagem extraída para obter o image_hash
        image_hash = upload_image(ad_account_id, frame_image_path)
        
        # Carregue o vídeo e obtenha o ID correspondente
        video_id = upload_video(ad_account_id, video_path)
        
        # Crie o anúncio com o vídeo específico
        creative = create_ad_creative(ad_account_id, video_id, image_hash, j) 
        ad = create_ad(ad_account_id, ad_set['id'], creative) 


print(f"Created Campaign ID: {campaign['id']}")


