import os
import json
import shutil

from modules import scripts, script_callbacks, shared
from . import util

root_path = os.getcwd()
extension_base = scripts.basedir()
# extension_base = os.path.join("extensions","civitai-shortcut")

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68'}

Extensions_Name = "Civitai Shortcut"

PLACEHOLDER = "<no select>"
NORESULT = "<no result>"  

CREATE_MODEL_FOLDER = "Create Model Name Folder"    

model_exts = (".bin", ".pt", ".safetensors", ".ckpt")

# civitai model type -> folder path
model_folders = {
    'Checkpoint': os.path.join("models","Stable-diffusion"),
    'LORA': os.path.join("models","Lora"),
    'LoCon': os.path.join("models","LyCORIS"),    
    'TextualInversion': os.path.join("embeddings"),   
    'Hypernetwork': os.path.join("models","hypernetworks"),         
    'AestheticGradient': os.path.join("extensions","stable-diffusion-webui-aesthetic-gradients","aesthetic_embeddings"),        
    'Controlnet': os.path.join("models","ControlNet"),
    'Poses': os.path.join("models","Poses"),
    'Wildcards': os.path.join("extensions","sd-dynamic-prompts","wildcards"),    
    'Other': os.path.join("models","Other"),    
    
    'VAE': os.path.join("models","VAE"),    
    'ANLORA': os.path.join("extensions","sd-webui-additional-networks","models","lora"),    
    'Unknown': os.path.join("models","Unkonwn"),
}

# UI 쪽에서 변환할때 쓰인다.
# UI model type -> civitai model type

# UI type 하나에 다중의 civitai type을 대입할때 대상이 되는것은  get_ui_typename 함수와 ishortcut->get_image_list 와 get_list 뿐이다.
# 나머지는 key로만 쓰이기 때문에 value 값이 배열이라 해도문제가 안될듯한다. 
# ishortcut 부분은 여기를
# tmp_types.append(setting.ui_typenames[sc_type])
# ->
# for type_name in setting.ui_typenames[sc_type]:
#     tmp_types.append(type_name)
# 이리 하면 될듯

# get_ui_typename는 이렇게 수정해도 문제 없을것 같다. 대신 모두 "" : ["",""] 형식으로 바꿔야 할듯(안해도 되나?)
# def get_ui_typename(model_type):
#     for k,v in ui_typenames.items():
#         if model_type in v:
#             return k
#     return model_type

ui_typenames = {
    "Checkpoint" : 'Checkpoint',
    "LoRA" : 'LORA',
    "LyCORIS" : 'LoCon',
    "Textual Inversion" : 'TextualInversion',
    "Hypernetwork" : 'Hypernetwork',
    "Aesthetic Gradient" : 'AestheticGradient',
    "Controlnet" : 'Controlnet',
    "Poses" : 'Poses',
    "Wildcards" : 'Wildcards',
    "Other" : 'Other',
}

#information tab 
civitai_information_tab = 0
saved_information_tab = 1
usergal_information_tab = 2
download_information_tab = 3

# civitai helper 호환성
info_ext = ".info"
info_suffix = ".civitai"

triger_ext = ".txt"
triger_suffix = ".triger"

preview_image_ext = ".png"
preview_image_suffix = ".preview"


# 갤러리 height 설정
information_gallery_height = "auto" # auto , fit

# 화면 분할 비율
shortcut_browser_screen_split_ratio = 4
shortcut_browser_screen_split_ratio_max  = 10

# 갤러리 ui설정
gallery_column = 7
shortcut_column = 5  
shortcut_count_per_page = 20
classification_gallery_column = 8

# 유저 갤러리 설정
usergallery_images_column = 6
usergallery_images_page_limit = 12
shortcut_max_download_image_per_version = 0 # 버전당 최대 다운로드 이미지 수 , 0이면 전체다운 받는다
gallery_thumbnail_image_style = "scale-down"

# 다운로드 설정
download_images_folder = os.path.join("outputs","download-images")

# 생성되는 폴더 및 파일
shortcut = "CivitaiShortCut.json"
shortcut_setting = "CivitaiShortCutSetting.json"
shortcut_classification = "CivitaiShortCutClassification.json"
shortcut_thumbnail_folder =  "sc_thumb_images"
shortcut_save_folder =  "sc_saves"
shortcut_info_folder =  "sc_infos"
shortcut_gallery_folder =  "sc_gallery"

no_card_preview_image = os.path.join(root_path,"html","card-no-preview.png")

shortcut_env = dict()

def init():
    global root_path
    global extension_base
    global model_folders
    
    global shortcut
    global shortcut_setting
    global shortcut_classification
    global shortcut_thumbnail_folder
    global shortcut_save_folder
    global shortcut_info_folder
    global shortcut_gallery_folder
    
    global shortcut_column
    global shortcut_count_per_page
    global gallery_column
    global classification_gallery_column
    global usergallery_images_column
    global usergallery_images_page_limit
    global shortcut_max_download_image_per_version
    global gallery_thumbnail_image_style

    global download_images_folder
    global shortcut_browser_screen_split_ratio
    global information_gallery_height
                            
    # root_path = os.getcwd()
       
    # util.printD(os.path.abspath(__file__))
    # util.printD(os.path.abspath(root_path))
    
    shortcut = os.path.join(extension_base,shortcut)
    shortcut_setting = os.path.join(extension_base,shortcut_setting)
    shortcut_classification = os.path.join(extension_base,shortcut_classification)
    shortcut_thumbnail_folder = os.path.join(extension_base,shortcut_thumbnail_folder)
    shortcut_save_folder = os.path.join(extension_base,shortcut_save_folder)
    shortcut_info_folder = os.path.join(extension_base,shortcut_info_folder)
    shortcut_gallery_folder = os.path.join(extension_base,shortcut_gallery_folder)
        
    if shared.cmd_opts.embeddings_dir:
        model_folders['TextualInversion'] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        model_folders['Hypernetwork'] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        model_folders['Checkpoint'] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        model_folders['LORA'] = shared.cmd_opts.lora_dir        
    
    environment = load()
    if environment:
        if "shortcut_browser_screen_split_ratio" in environment.keys():
            shortcut_browser_screen_split_ratio = int(environment['shortcut_browser_screen_split_ratio'])       
        if "information_gallery_height" in environment.keys():
            if environment['information_gallery_height'].strip():
                information_gallery_height = environment['information_gallery_height']

        if "shortcut_column" in environment.keys():
            shortcut_column = int(environment['shortcut_column'])
        if "shortcut_count_per_page" in environment.keys():
            shortcut_count_per_page = int(environment['shortcut_count_per_page'])
        if "gallery_column" in environment.keys():            
            gallery_column = int(environment['gallery_column'])
        if "classification_gallery_column" in environment.keys():
            classification_gallery_column = int(environment['classification_gallery_column'])
        if "usergallery_images_column" in environment.keys():
            usergallery_images_column = int(environment['usergallery_images_column'])
        if "usergallery_images_page_limit" in environment.keys():
            usergallery_images_page_limit = int(environment['usergallery_images_page_limit'])
        if "shortcut_max_download_image_per_version" in environment.keys():
            shortcut_max_download_image_per_version = int(environment['shortcut_max_download_image_per_version'])
        if "gallery_thumbnail_image_style" in environment.keys():
            gallery_thumbnail_image_style = environment['gallery_thumbnail_image_style']
            
        if "model_folders" in environment.keys():
                
            user_folders = environment['model_folders']
            
            if 'LoCon' in user_folders.keys():
                model_folders['LoCon'] = user_folders['LoCon']
            
            if 'Wildcards' in user_folders.keys():
                model_folders['Wildcards'] = user_folders['Wildcards']
                
            if 'Controlnet' in user_folders.keys():
                model_folders['Controlnet'] = user_folders['Controlnet']

            if 'AestheticGradient' in user_folders.keys():
                model_folders['AestheticGradient'] = user_folders['AestheticGradient']

            if 'Poses' in user_folders.keys():
                model_folders['Poses'] = user_folders['Poses']

            if 'Other' in user_folders.keys():
                model_folders['Other'] = user_folders['Other']

        if "download_folders" in environment.keys():
                
            download_folders = environment['download_folders']
            if 'download_images' in download_folders.keys():
                download_images_folder = download_folders['download_images']            
    
def generate_type_basefolder(content_type):
    
    if content_type in model_folders.keys():
        model_folder = model_folders[content_type]        
    elif content_type:
        model_folder = os.path.join(model_folders['Unknown'], util.replace_dirname(content_type))
    else:
        model_folder = os.path.join(model_folders['Unknown'])                    
                
    return model_folder
                
def generate_version_foldername(model_name,ver_name,ver_id):      
    # return f"{model_name}-{ver_name}-{ver_id}"
    return f"{model_name}-{ver_name}"

def get_model_folders():
    return model_folders.values()

def get_ui_typename(model_type):
    for k,v in ui_typenames.items():
        if v == model_type:
            return k
    return model_type
    
def get_modelid_from_shortcutname(sc_name):
    if sc_name:
        return sc_name[sc_name.rfind(':') + 1:]

def set_shortcutname(modelname,modelid):
    if modelname and modelid:
        return f"{modelname}:{modelid}"
    
def get_image_url_to_shortcut_file(modelid, versionid, image_url):
    if image_url:
        version_image_prefix = f"{versionid}-"
        model_path = os.path.join(shortcut_info_folder, str(modelid))      
        image_id, ext = os.path.splitext(os.path.basename(image_url))
        description_img = os.path.join(model_path, f"{version_image_prefix}{image_id}{preview_image_ext}")
        return description_img
    return None  

def get_image_url_to_gallery_file(image_url):
    if image_url:
        image_id, ext = os.path.splitext(os.path.basename(image_url))
        description_img = os.path.join(shortcut_gallery_folder, f"{image_id}{preview_image_ext}")
        return description_img
    return None  

def save(env):
    try:
        with open(shortcut_setting, 'w') as f:
            json.dump(env, f, indent=4)
    except Exception as e:
        return False
    
    return True

def load():
    if not os.path.isfile(shortcut_setting):        
        save({})
        return
    
    json_data = None
    try:
        with open(shortcut_setting, 'r') as f:
            json_data = json.load(f)
    except:
        pass

    return json_data
    
# def add_custom_type(custom_types):
    
#     global model_folders,ui_typenames        
    
#     model_folders[custom_types['model_type']] = custom_types['model_folder']
#     ui_typenames[custom_types['ui_typename']] = custom_types['model_type']
