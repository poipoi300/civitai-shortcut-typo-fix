import os
import gradio as gr
import modules.scripts as scripts

from modules import shared
from modules import script_callbacks

from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import model_action
from scripts.civitai_manager_libs import civitai_action

from scripts.civitai_manager_libs import ishortcut_action
from scripts.civitai_manager_libs import classification_action
from scripts.civitai_manager_libs import civitai_gallery_action

from scripts.civitai_manager_libs import civitai_shortcut_action

# def on_vs_folder_change(vs_folder):
#     return gr.update(visible=vs_folder)

def on_civitai_shortcut_tabs_select(evt: gr.SelectData, sc_types,sc_search,show_only_downloaded_sc):
    if evt.index == 1:        
        return ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search)
        
    return gr.update(visible=True)
        
def civitai_shortcut_ui():    
    with gr.Tabs(elem_id="civitai_shortcut_tabs_container") as civitai_tab:
        with gr.TabItem("Civitai Shortcut" , id="Shortcut"):
            with gr.Row(visible=False):
                #변수형 컨트롤
                #civitai model select model
                selected_version_id = gr.Textbox()
                selected_model_id = gr.Textbox()
                                
                # saved shortcut model select model
                selected_saved_version_id = gr.Textbox()
                selected_saved_model_id = gr.Textbox()

                # user gallery select model                        
                selected_usergal_model_id = gr.Textbox()
        
                # common                 
                refresh_sc_list = gr.Textbox(value="")                     
                selected_civitai_information_tabs = gr.Number(value=0, show_label=False)
                
            with gr.Row(): 
                with gr.Column(scale=1):
                    with gr.Tabs() as civitai_shortcut_tabs:
                        with gr.TabItem("Upload"):
                            with gr.Row(visible=False):                                 
                                register_information_only = gr.Checkbox(label="Register only model information", value=False)
                            with gr.Row():
                                with gr.Column():
                                    # with gr.Box(elem_classes="cs_box"):
                                    civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"])
                                    shortcut_saved_update_btn = gr.Button(value="Update Shortcut's Model Information",variant="primary")
                                    scan_to_shortcut_btn = gr.Button(value="Scan Downloaded Models to Shortcut",variant="primary")
                                    thumb_progress = gr.Markdown(value="###", visible=True)
                                    scan_progress = gr.Markdown(value="###", visible=True)
                                    update_modelfolder_btn = gr.Button(value="Update Downloaded Model Information", variant="primary")
                            with gr.Row(visible=False):
                                upload_progress = gr.Markdown(value="###", visible=False)
                                                                
                        with gr.TabItem("Browsing"):    
                            with gr.Row():
                                with gr.Column():
                                    shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)
                                    sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags ....",interactive=True, lines=1)
                                    sc_gallery = gr.Gallery(label="SC Gallery", elem_id="sc_gallery", show_label=False, value=ishortcut_action.get_thumbnail_list()).style(grid=[setting.shortcut_colunm], height="auto")
                                    show_only_downloaded_sc = gr.Checkbox(label="Show downloaded model's shortcut only", value=False)
                                    # refresh_sc_btn = gr.Button(value="Refresh Shortcut List",variant="primary")                                                              
                                
                        with gr.TabItem("Scan New Version"):
                            with gr.Row():
                                with gr.Column():
                                    shortcut_new_version_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)                                     
                                    scan_new_version_btn = gr.Button(value="Scan new version model", variant="primary")
                                    sc_new_version_gallery = gr.Gallery(label="SC New Version Gallery", elem_id="sc_new_version_gallery", show_label=False).style(grid=[setting.shortcut_colunm],height="auto")
                            
                with gr.Column(scale=4):
                    with gr.Tabs() as civitai_information_tabs:
                        with gr.TabItem("Civitai Model Information" , id="civitai_info"):
                            with gr.Row():
                                civitai_action.on_ui(selected_version_id,selected_model_id,refresh_sc_list)
                                
                        with gr.TabItem("Saved Model Information" , id="saved_info"):
                            with gr.Row():
                                ishortcut_action.on_ui(selected_saved_version_id,selected_saved_model_id,refresh_sc_list)
                                
                        with gr.TabItem("Civitai User Gallery" , id="gallery_info"):
                            with gr.Row():
                                civitai_gallery_action.on_ui(selected_usergal_model_id)      
        
        # with gr.TabItem("Manage" , id="Manage"):
        #     with gr.Tabs() as civitai_manage_tabs:        
        #         with gr.TabItem("Classification"):   
        #             with gr.Row():          
        #                 classification_action.on_ui()

    ###### Civitai Tab ######   
    civitai_shortcut_tabs.select(
        fn=on_civitai_shortcut_tabs_select,
        inputs=[
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,            
            ],
        outputs=[
            sc_gallery,
        ]    
    )
    
    # civitai upload tab start
    civitai_internet_url.upload(
        fn=civitai_shortcut_action.on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            register_information_only,
            selected_civitai_information_tabs
        ],
        outputs=[
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id,
            upload_progress,
            civitai_internet_url
        ]
    )
    
    scan_to_shortcut_btn.click(
        fn=civitai_shortcut_action.on_scan_to_shortcut_click,
        inputs=None,
        outputs=[
            scan_progress,
        ]                
    )
    
    shortcut_saved_update_btn.click(
        fn=civitai_shortcut_action.on_shortcut_saved_update_btn,
        inputs=None,
        outputs=[
            thumb_progress,
        ]
    ) 
    
    update_modelfolder_btn.click(
        fn=civitai_shortcut_action.on_update_modelfolder_btn_click,
        inputs=None,
        outputs=refresh_sc_list
    )
    
    thumb_progress.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
            thumb_progress
        ]
    )
    
    scan_progress.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
            scan_progress
        ]
    )
    
    upload_progress.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
            upload_progress,
        ]        
    )
    # civitai upload tab end
    
    # civitai browsing tab start
    shortcut_type.change(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,            
            sc_search,
            show_only_downloaded_sc,            
        ],
        outputs=[
            sc_gallery,
        ]
    )  
    
    sc_search.submit(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[            
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,                        
        ],
        outputs=[
            sc_gallery
        ]        
    )
    
    # refresh_sc_btn.click(
    #     fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
    #     inputs=[
    #         shortcut_type,
    #         sc_search,
    #         show_only_downloaded_sc,
    #     ],
    #     outputs=[
    #         sc_gallery
    #     ]
    # )    
        
    sc_gallery.select(civitai_shortcut_action.on_sc_gallery_select,selected_civitai_information_tabs,[selected_model_id,selected_saved_model_id,selected_usergal_model_id])    
    
    show_only_downloaded_sc.change(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
        ]
    )    
    # civitai browsing tab end
    
    # civitai scan new version tab start
    scan_new_version_btn.click(
        fn=civitai_shortcut_action.on_scan_new_version_btn,
        inputs=[
            shortcut_new_version_type,
        ],
        outputs=[
            sc_new_version_gallery,
        ]                
    )
    
    sc_new_version_gallery.select(civitai_shortcut_action.on_sc_gallery_select,selected_civitai_information_tabs,[selected_model_id,selected_saved_model_id,selected_usergal_model_id])
    # civitai scan new version tab end

    # Common start
    civitai_information_tabs.select(
        fn=civitai_shortcut_action.on_civitai_information_tabs_select,
        inputs=[
            selected_civitai_information_tabs,
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id
        ],
        outputs=[
            selected_civitai_information_tabs,
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id     
        ]
    )
    
    # sc 메뉴를 갱신시킨다.
    refresh_sc_list.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            # shortcut_downloaded_type,
            # sc_downloaded_search
        ],
        outputs=[
            sc_gallery,
            # sc_downloaded_gallery,
            refresh_sc_list
        ]
    )
    # Common end
    ###### Civitai Tab ###### 
            
def init_civitai_shortcut():
   
    setting.root_path = os.getcwd()
    
    if shared.cmd_opts.embeddings_dir:
        setting.model_folders[setting.model_types['textualinversion']] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        setting.model_folders[setting.model_types['hypernetwork']] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        setting.model_folders[setting.model_types['checkpoint']] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        setting.model_folders[setting.model_types['lora']] = shared.cmd_opts.lora_dir
        setting.model_folders[setting.model_types['locon']] = shared.cmd_opts.lora_dir
    
    setting.shortcut = os.path.join(scripts.basedir(),setting.shortcut)
    setting.shortcut_classification = os.path.join(scripts.basedir(),setting.shortcut_classification)
    setting.shortcut_thumbnail_folder = os.path.join(scripts.basedir(),setting.shortcut_thumbnail_folder)
    setting.shortcut_save_folder = os.path.join(scripts.basedir(),setting.shortcut_save_folder)
    setting.shortcut_info_folder = os.path.join(scripts.basedir(),setting.shortcut_info_folder)
    
    # 소유한 모델을 스캔하여 저장한다.
    model_action.Load_Downloaded_Models()
               
# init
init_civitai_shortcut()

def on_ui_tabs():
    # with gr.Blocks(analytics_enabled=False) as civitai_shortcut:
    with gr.Blocks() as civitai_shortcut:
        civitai_shortcut_ui()
    
    return (civitai_shortcut, "Civitai Shortcut", "civitai_shortcut"),


script_callbacks.on_ui_tabs(on_ui_tabs)
