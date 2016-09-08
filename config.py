#!/usr/bin/env python


class Config():
    default_subject = 'eecs'

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"

    smart_link_engin = 'amazon'

    #default_library = ''
    default_library = 'neuroscience-library'
    #default_library = 'cognitive-library'
    #default_library = 'health-library'
    #default_library = 'energy-library'
    #default_library = 'defense-library'
    #default_library = 'universe-library'
    #default_library = 'business-library'
    #default_library = 'frontier-library'
    #default_library = 'research-tool-library'

    #show random preview when click nav link
    track_mode = False

    disable_default_engin = True
  
    disable_thumb = "false"

    disable_icon = True

    disable_star_engin = False

    disable_reference_image = False 
   
    hiden_record_id = True
    hiden_record_id_commandline = False

    hiden_engins = True
    
    center_content = False
    
    content_margin_left = '15px'
    content_margin_top = '10px'
    split_height = '2px'

    #do not show nav links, only show extension links
    extension_mode = False

    default_tab = 'content'
    second_default_tab = ''#'figures'


    column_num = "1"
    custom_cell_len = 88 
    split_length = custom_cell_len + 15
    custom_cell_row = 5
    cell_len=89  #  cell_len >= course_num_len + 1 + course_name_len + 3
    course_name_len=70
    course_num_len=10
    color_index=0
    output_with_color = False
    output_with_style = False
    output_with_describe = False
    output_navigation_links = False
    merger_result = False
    top_row = 0
    old_top_row = 0
    max_links_row = 10
    max_nav_link_row = 11
    max_nav_links_row = 7
    default_links_row = 2    

    css_style_type = 0
    plugins_mode = False

    recommend_engin = True
    recommend_engin_num = 18

    auto_library_cell_len = False

    display_all_library = True

    
    background = ''

    fav_links = { 'papers' : ip_adress + '/?db=eecs/papers/&key=?',\
		  'civilization' : ip_adress + '/?db=other/&key=civilization2016&column=2',\
                  'bioRxiv' : 'cshsymposium.com/biorxiv/chartdailydetail.php',\
		  #'github' : ip_adress + '/?db=eecs/projects/github/&key=?',\
                  'rss' : ip_adress + '/?db=rss/&key=rss2016',\
                  #'rank' : ip_adress + '/?db=rank/&key=?',\
		  'youtube' :  ip_adress + '/?db=videos/&key=youtube2016&column=3'}
		  #'eecs' :  ip_adress + '/?db=eecs/&key=?'}
                  #'library' : ip_adress + '/?db=library/&key=?'}
		  #'neuroscience' : ip_adress + '/?db=neuroscience/&key=?'}
