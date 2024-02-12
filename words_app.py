# language learning App aimed to help learn languages.
# As example was chosen Danish an English
# Features: treating of text, splitting it to separated words, possibilities to chose particular word from the
# text and add it into the dictionary
# Translation was occurred via GoogleTranslate API with educational purpose
# Structure, hierarchy is:
# Main Window with 4 buttons can lead us to:
# --- screen with lists of words
# --- screen with popup window to add separate words, sentences with possibilities to treat it, split to words,
#       insert into table and chose wished ones
# --- screen with possibilities to add long snipped of text. Pressing on particular word we can achieve its highlighting
#       and add them into table and dictionary after
#     both upper screens create lists of word, pressing on which we can get into words set. You can read it as lines
#     or turn it into swiper card view pressing on it.
# --- screen with settings
# project is not finished and can be converted into different way.

import json
import os
import re
from deep_translator import GoogleTranslator
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton, MDIconButton, MDRectangleFlatButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem, IconLeftWidget, OneLineAvatarIconListItem, \
	OneLineRightIconListItem, ThreeLineListItem, TwoLineListItem, MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem, MDNavigationDrawer, MDNavigationDrawerHeader
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.swiper import MDSwiperItem, MDSwiper
from kivy.core.window import Window
from kivymd.uix.tooltip import MDTooltip

KV = '''
Intro:

    ScreenManager:
        id: sm

        Main_window: 

        List_box:
            id: lb

        Words_collection:
            id: w_col   

        Card_view:
            id: card_view

            #MySwiper:         
            #    id: my_swiper

        Add_article:
            id: add_article
		
		Set:
			id: settings
			
<Main_window>:
    name: "main_window"
    canvas.before:                    
        Color:                        
            rgba: 1, 1, 1, 0.1    
        Rectangle:                    
            size: self.size#self.height/2, self.height/2           
            pos: self.pos#self.width/2-150, self.height/2-150
            source: "background.png"

    MDGridLayout:
        size_hint: 0.75, 0.75
        pos_hint: {"center_x": 0.53, "center_y": 0.55}
        cols: 3
        rows: 3
        padding: [10,10,10,10]
        spacing: [15]
        #rows_minimum: {"0": 0.2, "1": 0.2}
        Button:
            pos_hint: {"center_x": 0.25, "center_y": 0.75}
            size_hint: None, None   
            size: 200, 100 #self.x, self.y
            #text: "lists of words"
            spacing: [10]
            background_normal: "lists.png" 
            on_press:                                      
                root.manager.current = "lists"  
                root.manager.transition.direction ='left'                       
        
        Widget: 
       
        Button:
            pos_hint: {"center_x": 0.75, "center_y": 0.75}
            size_hint: None, None   
            size: 200, 100
            rounded_button: False
            #text: "go_to_list"
            spacing: [10]
            background_normal: "words2.png"
        
            on_press: 
                root.manager.current = "words_collection"
                root.manager.transition.direction ='left'                   
        Widget:
        Widget:
        Widget:
        Button:
            pos_hint: {"center_x": 0.25, "center_y": 0.25}
            size_hint: None, None   
            size: 200, 100
            rounded_button: False
            
            spacing: [10]
            background_normal: "add_article.png"
            on_press:
                root.manager.current = "add_article"
                root.manager.transition.direction ='left' 
        Widget:
        Button:                                                          
            pos_hint: {"center_x": 0.75, "center_y": 0.25}               
            size_hint: None, None
            size: 200, 100                                        
            rounded_button: False                                        
                                                   
            spacing: [10]                                                
            background_normal: "setting.png"                             
            on_press:                                                    
                root.manager.current = "set"       
                root.manager.transition.direction ='left'  

<List_box>:
    name: "lists"                                                                                                                                                                                                             
    MDTopAppBar:
        id: "info_box" 
        title: "Lists of words"                                                                                                                                                                       
        elevation: 4                                                                         
        pos_hint: {"top": 1}                                                                 
        md_bg_color: "#e7e4c0"                                                               
        specific_text_color: "#4a4939"
                                                                                            	
    MDFloatLayout:
        TooltipMDIconButton:
            id: "tiptext"                          
            icon: "information"                        
            tooltip_text: str("""Lists of saved words. Are shown as title. Press on it and you will go further to words set""")
            #on_press: root.show_info()                                                      
            pos_hint: {"center_x": .95, "center_y": .94} 
        
    MDBoxLayout:
        orientation: "vertical"                                                                             
        size_hint: 1, 0.9                                                                    
        pos_hint_y: 0.1                                                                      
        MDScrollView:                                                                                                                                             
            MDList:                                                                          
                id: lists                                                                                                                                                         
	
		MDFloatLayout:                                                                           
		    size_hint: 1, 0.1
		                                                              
		    id: button_box                                                                       
		    MDRectangleFlatButton:                                                               
		        pos_hint: {"center_x": 0.35, "center_y": 0.5}                                    
		        text: "add list"                                                                 
		        on_press: root.add_list()                                                        
		    MDRectangleFlatButton:                                                               
		        pos_hint: {"center_x": 0.65, "center_y": 0.5}                                    
		        text: "del list"                                                                 
		        on_press: root.del_list()
		    MDFloatingActionButton:                            
		        icon: "arrow-left"                                
		        type: "small"                                  
		        pos_hint: {"center_x": 0.96, "center_y": 0.5}
		        on_press: 
		            root.manager.current =  "main_window"
		            root.manager.transition.direction ='right'                                                           
    MDBoxLayout:                                                                             
        size_hint: 1, 0.1

<Words_collection>:
    name: "words_collection"
    MDTopAppBar:
        title: "Add new words"
        elevation: 4
        pos_hint: {"top": 1}
        md_bg_color: "#e7e4c0"
        specific_text_color: "#4a4939"
        left_action_items:
            [['menu', lambda x:(nav_drawer.set_state("open"), root.add_items_to_menu())]]
        
    MDFloatLayout:
        pos_hint: {"center_x": 0.5, "center_y": 0.94}
	    TooltipMDIconButton:
	        id: "tiptext"                          
	        icon: "information"                        
	        tooltip_text: str("""Add words and create your own list""")
	        #on_press: root.show_info()                                                      
	        pos_hint: {"center_x": .95, "center_y": .5} 
        
             
    MDBoxLayout:
        orientation: "vertical"

        size_hint: 1, 0.9
        pos_hint_y: 0.1
        MDScrollView:      

            MDList:
                id: words_list

        MDFloatLayout:
            size_hint: 1, 0.1 
            id: button_box
            canvas:                                    
                Color:                                 
                    rgba: 0.25, 0.1, 1, 0.15           
                Rectangle:                             
                    size: self.size                    
                    pos: self.pos                      

            MDRectangleFlatButton:
                pos_hint: {"center_x": 0.35, "center_y": 0.5}
                text: "add word"
                on_press: root.add_word()
            MDRectangleFlatButton:                          
                pos_hint: {"center_x": 0.65, "center_y": 0.5}
                text: "del word"                            
                on_press: root.del_word()
            MDFloatingActionButton:                            
                icon: "arrow-left"                                
                type: "small"                                  
                pos_hint: {"center_x": 0.96, "center_y": 0.5}
                on_press:
                    root.save_data() 
                    #root.manager.current =  "main_window"
                    #root.manager.transition.direction ='right'  
    MDBoxLayout:
        size_hint: 1, 0.1    

    CustomMDNavigationDrawer:
        id: nav_drawer

<MDNavigationDrawer@CustomMDNavigationDrawer>:                             
    #id: nav_drawer                                    
    radius: (0, 0, 0, 0)                              
    #md_bg_color: "#e7e4c0"
    #status: 'closed'
    #on_status: root.on_status(self.status)

    MDBoxLayout:
        orientation: "vertical"                           
        ContentNavigationDrawer:

            MDNavigationDrawerMenu:                       
                id: navigation_menu                       

                MDNavigationDrawerHeader:                 
                    title: "List sets"                    
                    title_color: "#4a4939"                
                    text: "Collection"                    
                    spacing: "4dp"                        
                    padding: "12dp", 0, 0, "56dp"                    

        MDFloatLayout:
            size_hint: 1, 0.1
            pos_hint: {"x": 0, "y": 0} 
            MDFloatingActionButton:                         
                icon: "plus"                             
                type: "small"                               
                pos_hint: {"center_x": 0.5, "center_y": 0.25}
                on_press: root.add_line()                
                                                                                 
<BottomBar>:
    MDBoxLayout:
        #size_hint: 1, 0.5
        MDBottomNavigation:
            size_hint: 1, 0.05
        #panel_color: "#eeeaea"
            selected_color_background: "orange"
            text_color_active: "lightgrey"

            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'Mail'
                icon: 'gmail'
                badge_icon: "numeric-10"

            MDBottomNavigationItem:
                #name: 'screen 2'
                #text: 'Twitter'
                #icon: 'twitter'
                #badge_icon: "numeric-5"
                MDRectangleFlatButton:                          
                    #pos_hint: {"center_x": 0.65, "center_y": 0.1}
                    text: "del word"                            
                    #on_press: root.del_word()          
            MDBottomNavigationItem:
                #name: 'screen 3'
                #text: 'LinkedIN'
                #icon: 'linkedin'                                                                                           
                MDRectangleFlatButton:
                    #pos_hint: {"center_x": 0.35, "center_y": 0.1}
                    text: "add word"
                    #on_press: root.add_word()

<Content>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: input_text
        hint_text: "List name"
        mode: "rectangle"

    MDBoxLayout:
        MDLabel: 
            text: "words list"

<Content_words>:
    #orientation: "vertical"
    size_hint_y: None  
    height: "300dp"    
    #size: self.size
    MDTextField:
        id: input_text
        text: self.text                                               
        size_hint: 1, None                                     
        height: "30dp"                                         
        pos_hint: {"center_x": 0.5, "center_y": 0.85}          
        hint_text: "Put whole sentence in"                                      
        multiline: True                                        
        mode: "rectangle" 
                                             
    MDBoxLayout:
        #id: word_box
        size_hint: 1, None
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        height: "200dp" 
        canvas:
            Color:
                rgba: 0.25, 0.1, 1, 0.15
            Rectangle:        
                size: self.size
                pos: self.pos
        MDScrollView:
            MDList:
                id: word_box
<Content_save_lst>:
    size_hint_y: None   
    height: "100dp"     
    MDTextField:
        size_hint: 1, None                             
        height: "30dp"                                 
        pos_hint: {"center_x": 0.5, "center_y": 0.85}  
        id: title_text
        hint_text: "title"

<MySwiper>:                                   


    MDAnchorLayout:
        anchor_x: "center"
        anchor_y: "center"

        MDCard:
            id: card      
                                      
            pos_hint: {"center_x": 0.5, "center_y": 0.5}                                                                                        
            #padding: 4                                                                        
            size_hint: None, None                                                                     
            size: "500dp", "350dp"                                                                    

            line_color: (0.2, 0.2, 0.2, 0.5)                                                          
            style: "elevated"      # could be elevated                                                                   
            md_bg_color: "#f6eeee"                                                                    
            shadow_offset: (0, -1)

            MDRelativeLayout:                                                                                                                                                      
                id: card_box          
                MDIconButton:                                                                         
                    icon: "dots-vertical"                                                             
                    pos_hint: {"top": 1, "right": 1}                                                                                                                                   
                MDLabel:                                                                              
                    id: label                                                                         
                    text: "text"                                                                      
                    adaptive_size: True                                                               
                    color: "grey"                                                                     
                    pos: "12dp", "12dp"                                                               
                    bold: True                                                                        
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}                                      
                MDRectangleFlatButton:                                                                
                    text: "Yes"                                                                       
                    pos_hint: {"center_x": 0.2, "center_y": 0.1}                                      
                    line_color: 0, 0, 0, 0
                    on_press: app.root.ids.card_view.yes()                                                            
                MDFloatingActionButton:                                                               
                    icon: "android"                                                                   
                    type: "small"                                                                     
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}                                      
                    line_color: 0, 1, 0, 0.75
                    on_press: app.root.ids.card_view.translate()                                                           
                MDRectangleFlatButton:                                                                
                    text: "No"                                                                        
                    pos_hint: {"center_x": 0.8, "center_y": 0.1}                                      
                    line_color: 0, 0, 0, 0
                    on_press: app.root.ids.card_view.no()
       
       

<Card_view>:

    name: "cards"
    MDTopAppBar:                                                                             
        #size_hint: 1, 0.1                                                                   
        title: "Navigation Drawer"                                                           
        elevation: 4                                                                         
        pos_hint: {"top": 1}                                                                 
        md_bg_color: "#e7e4c0"                                                               
        specific_text_color: "#4a4939"  
		right_action_items: [ ["information", lambda x: x]]
    MDFloatLayout:
        id: swiper
        size_hint: 1, 1                                
        pos_hint: {"center_x": 0.5, "center_y": 0.75}

    MDFloatLayout:
        name: "my_float_layout"
        size_hint: 1, 0.1 
        id: button_box
        canvas:                                    
            Color:                                 
                rgba: 0.25, 0.1, 1, 0.15           
            Rectangle:                             
                size: self.size                    
                pos: self.pos                      

        MDRectangleFlatButton:
            pos_hint: {"center_x": 0.35, "center_y": 0.5}
            text: "add word"
            #on_press: root.add_word()
        MDRectangleFlatButton:                          
            pos_hint: {"center_x": 0.65, "center_y": 0.5}
            text: "del word"                            
            #on_press: root.del_word()
        MDFloatingActionButton:                            
            icon: "arrow-left"                             
            type: "small"                                  
            pos_hint: {"center_x": 0.96, "center_y": 0.5}  
            on_press:
                #root.save_data() 
                root.manager.current =  "lists"
                root.manager.transition.direction ='right'

<Add_article>:
    name: "add_article"
    MDTopAppBar:
        #size_hint: 1, 0.1
        title: "Add article"
        elevation: 4
        pos_hint: {"top": 1}
        md_bg_color: "#e7e4c0"
        specific_text_color: "#4a4939"
        left_action_items:
            [['menu', lambda x:(nav_drawer.set_state("open"), root.add_items_to_menu())]]     
		
	MDFloatLayout:                                                         
	    pos_hint: {"center_x": 0.5, "center_y": 0.94}                      
	    TooltipMDIconButton:                                               
	        id: "tiptext"                                                  
	        icon: "information"                                            
	        tooltip_text: str("""Insert text and create a word set""")    
	                                         
	        pos_hint: {"center_x": .95, "center_y": .5}                    	
    MDAnchorLayout:
        anchor_x: "center"
        anchor_y: "center"
        id: text_box
        size_hint: 0.9, 0.85
        pos_hint: {"center_x": 0.47, "center_y": 0.5}                                                                                   

        MDTextFieldRect:
            id: text_inp                                      
            size_hint: 1, 0.85                               
            multiline: True                                   
            pos_hint: {"center_x": 0.5, "center_y": 0.3}      

    MDFloatingActionButton:                               
        icon: "plus"                                      
        type: "small"                                     
        pos_hint: {"center_x": 0.96, "center_y": 0.2}     
        on_press:                                        
            root.text_to_label()                          

    MDFloatLayout:
        size_hint: 1, 0.1 
        id: button_box
        canvas:                                    
            Color:                                 
                rgba: 0.25, 0.1, 1, 0.15           
            Rectangle:                             
                size: self.size                    
                pos: self.pos                      

        MDFloatingActionButton:                            
            icon: "arrow-left"                                
            type: "small"                                  
            pos_hint: {"center_x": 0.96, "center_y": 0.5}
            on_press:
                #root.save_data() 
                root.manager.current =  "main_window"
                root.manager.transition.direction ='right'

	CustomMDNavigationDrawer:
	    id: nav_drawer       

<Add_article_pop_up_window_content>:

    size_hint_y: None
    height: "400dp"

    MDFloatLayout:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        MDTextField:                                           
            id: Article_name                       
            pos_hint: {"center_x": 0.5, "center_y": 0.95}       
            hint_text: "enter article name"                    
            #font_size: 20                                     
            #size_hint: 0.8, 0.1
            #size: self.width, self.height                               

        MDScrollView:                                          
            size_hint: 1, 0.9                                 
            pos_hint: {"center_x": 0.5, "center_y": 0.4}       
            MDList:                                            
                id: word_list_article                                               
                #TwoLineIconListItem:                           
                #    text: "Headline"                           

<Set>:
	name: "set"	
	MDTopAppBar:                                                                                         
	                                                                                  
	    title: "Settings"                                                                             
	    elevation: 4                                                                                     
	    pos_hint: {"top": 1}                                                                             
	    md_bg_color: "#e7e4c0"                                                                           
	    specific_text_color: "#4a4939"                                                                                           
        right_action_items: [ ["information", lambda x: x]]                                                                                             
	MDAnchorLayout:                                                                                      
	    anchor_x: "center"                                                                               
	    anchor_y: "top"                                                                               
	    id: text_box                                                                                     
	    size_hint: 0.9, 0.85                                                                             
	    pos_hint: {"center_x": 0.5, "center_y": 0.45}                                                    
		MDList:
			OneLineListItem:
				id: first_line
		        pos_hint: {"center_x": .5, "center_y": .5}
		        size_hint_x: .8
		        text: "Set original language"
		       
				MDDropDownItem:
					id: org_lang
				    pos_hint: {"center_x": 0.95, "center_y": .5}  
				    text: 'lang'
				    on_press: root.set_org_lang()
		        
		        
		        
			OneLineListItem:
		        pos_hint: {"center_x": .5, "center_y": .5}
		        size_hint_x: .8
		        text: "Set target language"
		        MDDropDownItem:
		            id: target_lang                                    
		            pos_hint: {"center_x": 0.95, "center_y": .5}   
		            text: 'lang'                                   
		            on_press: root.set_target_lang()                      
		        
			OneLineListItem:
		        pos_hint: {"center_x": .5, "center_y": .5}
		        size_hint_x: .8
		        text: "Set theme color"
			    MDDropDownItem:
			        id: theme                                    
			        pos_hint: {"center_x": 0.95, "center_y": .5}   
			        text: 'theme'                                   
			        on_press: root.change_style()                      
				
			
	MDFloatLayout:                                                                                       
	    size_hint: 1, 0.1                                                                                
	    id: button_box                                                                                   
	    canvas:                                                                                          
	        Color:                                                                                       
	            rgba: 0.25, 0.1, 1, 0.15                                                                 
	        Rectangle:                                                                                   
	            size: self.size                                                                          
	            pos: self.pos                                                                            
	
	    MDRectangleFlatButton:                                                                           
	        pos_hint: {"center_x": 0.35, "center_y": 0.5}                                                
	        text: "OK"                                                                             
	                                                                           
	    MDRectangleFlatButton:                                                                           
	        pos_hint: {"center_x": 0.65, "center_y": 0.5}                                                
	        text: "Back"                                                                             
	        on_press:
	            root.manager.current =  "main_window"
                root.manager.transition.direction ='right'                                                                  


<TooltipMDIconButton@MDIconButton+MDTooltip>    
'''

class Intro(MDBoxLayout):
	pass

# main window class
class Main_window(MDScreen):
	pass

class RightCheckbox(IRightBodyTouch, MDCheckbox):
	pass

class ContentNavigationDrawer(MDBoxLayout):
	pass

class CustomMDNavigationDrawer(MDNavigationDrawer):
	pass

class Content(MDFloatLayout):
	pass

class YourContainer(IRightBodyTouch, MDBoxLayout):
	adaptive_width = True

class Content_words(MDFloatLayout):
	pass

class Content_save_lst(MDBoxLayout):
	pass
# words screen class implementation
class Words_collection(MDScreen):
	dialog = None
	dialog_1 = None

	def __init__(self, **kwargs):
		super(Words_collection, self).__init__(**kwargs)
		self.list_box = List_box()
		self.root = Intro()
		self.content = Content_words()
		self.content_save_lst = Content_save_lst()
		self.sm = ScreenManager()
	# call a popup window to add words or sentence
	def add_word(self):
		if not self.dialog:
			self.dialog = MDDialog(
				type="custom",
				content_cls=self.content,
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						on_press=self.clean_box

					),
					MDFlatButton(
						text="OK",
						theme_text_color="Custom",
						on_press=self.split_to_words,

					),
				],
			)
		self.dialog.open()
	# delete added words
	def del_word(self):
		active_items = []
		for i in range(len(self.ids.words_list.children)):
			check_box = RightCheckbox()
			self.ids.words_list.children[i].add_widget(check_box)

		self.ids.button_box.add_widget(MDFloatingActionButton(
			size_hint = (0.06, 0.8),
			rounded_button=False,
			type="standard",
			icon="delete",
			pos_hint=({"center_x": 0.85, "center_y": 0.5}),
			size = (20, 20),
			id="float_button",
			on_press=self.del_active_items
		))

	def del_active_items(self, instance):
		active_items = []
		for i in range(len(self.ids.words_list.children)):
			check_box = self.ids.words_list.children[i].children[0].children[0]
			# print(check_box)
			if isinstance(check_box, RightCheckbox) and check_box.active:
				active_items.append(i)

		# print(active_items)
		for index in reversed(active_items):
			self.ids.words_list.remove_widget(self.ids.words_list.children[index])

		for i in range(len(self.ids.words_list.children)):
			for widget in self.ids.words_list.children[i].children[0].children:
				if isinstance(widget, RightCheckbox):
					self.ids.words_list.children[i].children[0].remove_widget(widget)

		for child in self.ids.button_box.children:
			if isinstance(child, MDFloatingActionButton):
				self.ids.button_box.remove_widget(child)
				break

		checkboxes_to_remove = [child for child in self.ids.words_list.children if isinstance(child, RightCheckbox)]
		for checkbox in checkboxes_to_remove:
			self.ids.words_list.remove_widget(checkbox)

	#add items to the navigation drawer menu which evokes with top up left corner menu button
	def add_items_to_menu(self):
		folder_path = r'C:\Users\admin\PycharmProjects\smart_home\cards'
		# List all files in the directory
		file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]

		for file_name in file_names:
			# Construct the full path for each file
			file_path = os.path.join(folder_path, file_name)
			# Split the file name and extension
			name_without_extension, _ = os.path.splitext(file_name)
			# Open and read the JSON file
			with open(file_path, 'r', encoding='utf-8') as file:
				data = json.load(file)

			if not any(item.text == name_without_extension for item in
			           self.ids.nav_drawer.ids.navigation_menu.children[0].children):
				self.ids.nav_drawer.ids.navigation_menu.add_widget(MDNavigationDrawerItem(
					icon="book",
					text=name_without_extension
				))

	def on_press(self, instance):

		index = len(self.ids.nav_drawer.ids.navigation_menu.children[0].children) - 1 - \
		        self.ids.nav_drawer.ids.navigation_menu.children[0].children.index(instance)
		Words_app.get_running_app().root.ids.sm.current = f"words_collection_{index}"

	# splitting added words, sentence into separated words without punctuation signs
	def split_to_words(self, arg):

		text_to_translate = self.content.ids.input_text.text

		words_list = re.findall(r'\b[^\d\s.,\/-]+\b', text_to_translate)
		for self.i in words_list:
			# print(type(i))
			# word = str(i)
			self.content.ids.word_box.add_widget(
				OneLineRightIconListItem(
					YourContainer(

						MDIconButton(
							id="plus_button",
							icon="plus",
							on_press=self.select_word
						),
						id="container"
					),
					text=str(self.i)
				)
			)

	# selecting desired words pressing onto plus button
	def select_word(self, instance):
		for index, button_container in enumerate(self.content.ids.word_box.children):
			if instance in button_container.children[0].children[0].children:
				self.ids.words_list.add_widget(

					TwoLineListItem(
						text=self.content.ids.word_box.children[index].text,
						secondary_text=GoogleTranslator(source='da', target='en').translate(
							self.content.ids.word_box.children[index].text))

				)


	# save retrieved data into memory
	def save_data(self):
		if not self.dialog_1:
			self.dialog_1 = MDDialog(
				# with self.canvas:
				#     Color(rgba = (0.25, 0.1, 1, 0.25)),
				#     Rectangle(size = self.size, pos = self.pos)
				title="Save the word set into a list?",
				type="custom",
				content_cls=self.content_save_lst,
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						on_press=self.clean_box1
						# text_color=self.theme_cls.primary_color,
					),
					MDFlatButton(
						text="OK",
						theme_text_color="Custom",
						on_press=self.save_list,
						# text_color=self.theme_cls.primary_color
					),
				],
			)
		self.dialog_1.open()

	def save_list(self, newname):
		data_to_save = {}
		newname = self.content_save_lst.ids.title_text.text
		for child in self.ids.words_list.children:

			data_to_save[child.text] = child.secondary_text

		try:
			# Attempt to open the file for writing
			with open(f'{newname}.json', 'w', encoding='utf-8') as file:
				json.dump(data_to_save, file, ensure_ascii=False)

		except Exception as e:
			print(f"Error: {e}")

		Words_app.get_running_app().root.ids.sm.current = "main_window"

		Words_app.get_running_app().root.ids.sm.transition.direction = 'right'

		self.dialog_1.dismiss()
	# add card view opportunities
	def add_cards(self):

		Words_app.get_running_app().root.ids.sm.current = "card_view"

	def clean_box1(self, *args):
		self.content.ids.input_text.text = " "
		self.content.ids.word_box.clear_widgets()
		Words_app.get_running_app().root.ids.sm.current = "main_window"
		Words_app.get_running_app().root.ids.sm.transition.direction = "right"
		self.dialog_1.dismiss()

	def clean_box(self, *args):
		self.content.ids.input_text.text = " "
		self.content.ids.word_box.clear_widgets()
		Words_app.get_running_app().root.ids.sm.current = "main_window"
		Words_app.get_running_app().root.ids.sm.transition.direction = "right"
		self.dialog.dismiss()

class Content(MDBoxLayout):
	pass

class ScreenManager(ScreenManager):
	pass
# lists screen class
class List_box(MDScreen):
	dialog = None

	def __init__(self, **kwargs):
		super(List_box, self).__init__(**kwargs)
		self.content = Content()
		self.sm = ScreenManager()
		self.root = Intro()
		self.card_view = Card_view()
		# self.swiper_item = MySwiper()
		self.add_widget(self.sm)
		self.reference = ' '
	# reading off data from memory
	def on_pre_enter(self):
		folder_path = r'C:\Users\admin\PycharmProjects\smart_home\cards'

		# List all files in the directory
		file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]

		for file_name in file_names:
			# Construct the full path for each file
			file_path = os.path.join(folder_path, file_name)
			# Split the file name and extension
			name_without_extension, _ = os.path.splitext(file_name)
			# Open and read the JSON file
			with open(file_path, 'r', encoding='utf-8') as file:
				data = json.load(file)

			new_item = OneLineRightIconListItem(
				text=name_without_extension,

				on_press=self.refer_to_word_set)

			if not any(item.text == name_without_extension for item in self.ids.lists.children):
				self.ids.lists.add_widget(new_item)

		scr_numbers = len(file_names)
	# way to set with following words
	def refer_to_word_set(self, instance):

		index = len(self.ids.lists.children) - self.ids.lists.children.index(instance)

		# print(index)
		self.folder_path = rf'C:\Users\admin\PycharmProjects\smart_home\cards\{instance.text}.json'
		with open(self.folder_path, 'r', encoding='utf-8') as json_file:
			self.data = json.load(json_file)

		self.word_collection = Words_collection()
		self.word_collection.name = f"words_collection_{index}"

		for key, value in self.data.items():
			self.word_collection.ids.words_list.add_widget(TwoLineListItem(
				text=f"{key}",
				secondary_text=f"{value}",
				on_press=(self.go_to_cards)
			))
		self.card_view.add_card(instance)
		# self.reference = instance.text
		# print("here is reference: ", self.reference)#was used add_card method
		self.word_collection.ids.button_box.add_widget(MDRectangleFlatButton(
			text="<--",
			pos_hint={"center_x": 0.1, "center_y": 0.5},
			on_press=self.back_to_lists
		))

		Words_app.get_running_app().root.ids.sm.add_widget(self.word_collection)
		Words_app.get_running_app().root.ids.sm.current = f"words_collection_{index}"
		Words_app.get_running_app().root.ids.sm.transition.direction = "left"
	# back to lists
	def back_to_lists(self, arg):
		Words_app.get_running_app().root.ids.sm.current = "lists"
		Words_app.get_running_app().root.ids.sm.transition.direction = "right"
	# create new list
	def add_list(self):
		if not self.dialog:
			self.dialog = MDDialog(
				title="Address:",
				type="custom",
				content_cls=self.content,
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						# text_color=self.theme_cls.primary_color,
					),
					MDFlatButton(
						text="OK",
						theme_text_color="Custom",
						on_press=self.create_list,
						# text_color=self.theme_cls.primary_color,
					),
				],
			)
		self.dialog.open()

	def create_list(self, *args):

		scr_number = len(Words_app.get_running_app().root.ids.sm.screens) - 2
		new_words_screen = Words_collection(name=f"words_collection_{scr_number}")
		Words_app.get_running_app().root.ids.sm.add_widget(new_words_screen)


		def on_release(instance):
			index = len(self.ids.lists.children) - 1 - self.ids.lists.children.index(instance)
			screen_name = Words_app.get_running_app().root.ids.sm.screen_names[index + 2]
			# print(f"Pressed line item: {pressed_text}, index: {index}" )    debugging process in the console          Words_app.get_running_app().root
			Words_app.get_running_app().root.ids.sm.current = str(screen_name)

		self.list_item = OneLineRightIconListItem(

			text=self.content.ids.input_text.text,
			on_release=on_release
			# on_press = self.add_to_menu
		)

		self.ids.lists.add_widget(self.list_item)
		self.content.ids.input_text.text = ""
		self.dialog.dismiss()

	def del_list(self, *args):
		active_items = []
		
		for i in range(len(self.ids.lists.children)):

			check_box = RightCheckbox()
			self.ids.lists.children[i].add_widget(check_box)
		#print(self.ids.lists.children[0].children[0].children[3])
		self.ids.button_box.add_widget(MDFloatingActionButton(
			size_hint = (0.06, 0.75),
			# size = (30, 20),
			rounded_button=False,
			type="standard",
			icon="delete",
			pos_hint=({"center_x": 0.85, "center_y": 0.5}),
			id="float_button",
			on_press=self.del_active_items
		))
	# delete marked items
	def del_active_items(self, instance):
		active_items = []
		for i in range(len(self.ids.lists.children)):
			check_box = self.ids.lists.children[i].children[0].children[0]
			# print(check_box)
			if isinstance(check_box, RightCheckbox) and check_box.active:
				active_items.append(i)

		# print(active_items)
		for index in reversed(active_items):
			self.ids.lists.remove_widget(self.ids.lists.children[index])

		for i in range(len(self.ids.lists.children)):
			for widget in self.ids.lists.children[i].children[0].children:
				if isinstance(widget, RightCheckbox):
					self.ids.lists.children[i].children[0].remove_widget(widget)

		for child in self.ids.button_box.children:
			if isinstance(child, MDFloatingActionButton):
				self.ids.button_box.remove_widget(child)
				break

		checkboxes_to_remove = [child for child in self.ids.lists.children if isinstance(child, RightCheckbox)]
		for checkbox in checkboxes_to_remove:
			self.ids.lists.remove_widget(checkbox)
	# turn into cardview
	def go_to_cards(self, arg):

		app = Words_app.get_running_app()

		Words_app.get_running_app().root.ids.sm.current = "cards"

class ListTooltipClass(MDTooltip):
	pass

class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass

class MySwiper(MDFloatLayout):
	pass
# card view representation. Implementation of the screen
class Card_view(MDScreen):
	keys = []

	def __init__(self, **kwargs):
		super(Card_view, self).__init__(**kwargs)
		self.del_widget = None
		self.keys = []

	def add_card(self, instance):
		folder_path = rf'C:\Users\admin\PycharmProjects\smart_home\cards\{instance.text}.json'  # queen on resort       #{instance.text}
		with open(folder_path, 'r', encoding='utf-8') as json_file:
			self.data = json.load(json_file)
			print(self.data)
		for key in self.data.keys():
			self.swiper_item = MySwiper()
			self.swiper_item.ids.label.text = key
			self.swiper_item.ids.label.font_style = "H4"
			Card_view.keys.append(key)
			Words_app.get_running_app().root.ids.card_view.ids.swiper.add_widget(self.swiper_item)
	#reaction on perssing yes button
	def yes(self):

		swiper = Words_app.get_running_app().root.ids.card_view.ids.swiper.children[0]
		anim = Animation(x=-500, y=50, duration=0.5, t="in_out_sine")
		anim.start(swiper.ids.card)
		Clock.schedule_once(self.remove_card, 1)
	# reaction on pressing no button
	def no(self):
		swiper = Words_app.get_running_app().root.ids.card_view.ids.swiper.children[0]
		# anim = Animation(x=100, y=120, duration=0.5, t = "in_out_sine")
		anim = Animation(x=1000, y=50, duration=0.5, t="in_out_sine")
		# Start animation
		anim.start(swiper.ids.card)
		Clock.schedule_once(self.remove_card, 1)

	#def swipe_left(self):
	#	self.del_widget = self.children[1]
	#	# self.remove_widget(self.del_widget)
	#	self.relevant_index += 1
	#
	#def swipe_right(self):
	#	self.relevant_index += 1
	#	print("left: " + str(self.relevant_index))
	#calling of translation
	def translate(self):
		self.swiper_item = MySwiper()
		app = Words_app.get_running_app()
		word = app.root.ids.card_view.ids.swiper.children[0].children[0].children[0].children[0].children[3]
		translated_label = app.root.ids.card_view.ids.swiper.children[0].children[0].children[0].children[0]
		keys = Card_view.keys
		translated_text = GoogleTranslator(source='da', target='en').translate(word.text)
		print(translated_text)
		word.pos_hint = {"center_x": 0.5, "center_y": 0.65}

		print(translated_label)

		translation = MDLabel(text=translated_text,
			pos_hint={"center_x": 0.5, "center_y": 0.3},
			font_style="H4",
			halign="center",
			bold=True,
			color="grey"
		)

		translated_label.add_widget(translation)

	def remove_card(self, dt):
		swiper = Words_app.get_running_app().root.ids.card_view.ids.swiper.children[0]
		Words_app.get_running_app().root.ids.card_view.ids.swiper.remove_widget(swiper)
		print(swiper)

# adding article screen
class Add_article(MDScreen):
	dialog = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.pop_up_menu = Add_article_pop_up_window_content()
		self.root = Intro()
	#convert text into label
	def text_to_label(self, *args):
		text = self.ids.text_inp.text
		self.ids.text_box.clear_widgets()
		self.label = MDLabel(

			size_hint=(1, None),
			adaptive_height=True,
			pos_hint={"center_x": 0.5, "center_y": 0.5},
			markup=True,
			on_ref_press=self.on_ref_press
		)
		scroll_view = ScrollView(size_hint=(1, None),
			height=self.height * 0.75,
			pos_hint={"center_x": 0.5, "center_y": 0.5})

		scroll_view.add_widget(self.label)
		self.ids.text_box.add_widget(scroll_view)

		words = text.split()

		for word in words:
			self.label.text += f"[ref={word}]{word}[/ref] "

		self.clicked_words = {}

		button = MDFloatingActionButton(
			icon="check-circle-outline",
			type="small",
			pos_hint={"center_x": 0.96, "center_y": 0.3},
			on_press=self.call_pop_up_menu)
		self.add_widget(button)
	#callback on words pressing
	def on_ref_press(self, instance, value):
		# Callback when a word is clicked

		# print(f"Clicked on word: {value}")

		# Append the clicked word to the list


		# Change font size and color for the clicked word

		instance.text = instance.text.replace(
			f"[ref={value}]{value}[/ref]",
			f"[size=20][color=#FF0000][ref={value}]{value}[/ref][/color][/size]"
		)

		original_word = re.sub(r'[^\w\s]', '', value)  # .encode('utf-8')
		# original_word = original_word.encode('utf-8')
		translated_word = GoogleTranslator(source='da', target='en').translate(original_word)

		# print(original_word, translated_word)
		self.clicked_words[original_word] = translated_word
	# call popup menu with celected words and its translation
	def call_pop_up_menu(self, args):

		for key, value in self.clicked_words.items():
			self.pop_up_menu.ids.word_list_article.add_widget(TwoLineListItem(
				text=key,
				secondary_text=value
			)
			)
		if not self.dialog:
			self.dialog = MDDialog(
				title="Add new words set:",
				type="custom",
				content_cls=self.pop_up_menu,
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						# text_color=self.theme_cls.primary_color,
						on_press=lambda x: self.dialog.dismiss()
					),
					MDFlatButton(
						text="OK",
						theme_text_color="Custom",
						on_press=self.create_new_list,
						# text_color=self.theme_cls.primary_color,
					),
				],
			)
		self.dialog.open()
	# creating new dictionary
	def create_new_list(self, *args):

		folder_path = r'C:\Users\admin\PycharmProjects\smart_home\cards'

		# List all files in the directory
		file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]

		for file_name in file_names:
			# Construct the full path for each file
			file_path = os.path.join(folder_path, file_name)
			# Split the file name and extension
			name_without_extension, _ = os.path.splitext(file_name)
			# Open and read the JSON file
			with open(file_path, 'r', encoding='utf-8') as file:
				data = json.load(file)
		newname = self.pop_up_menu.ids.Article_name.text

		# print(data_to_save)
		try:
			# Attempt to open the file for writing
			with open(f'{newname}.json', 'w', encoding='utf-8') as file:
				json.dump(self.clicked_words, file, ensure_ascii=False)
		# print("Data saved successfully.")
		except Exception as e:
			print(f"Error: {e}")
		self.dialog.dismiss()
	# add items to navigation drawer menu
	def add_items_to_menu(self):

		folder_path = r'C:\Users\admin\PycharmProjects\smart_home\cards'

		# List all files in the directory
		file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]

		for file_name in file_names:
			# Construct the full path for each file
			file_path = os.path.join(folder_path, file_name)
			# Split the file name and extension
			name_without_extension, _ = os.path.splitext(file_name)
			# Open and read the JSON file
			with open(file_path, 'r', encoding='utf-8') as file:
				data = json.load(file)

			if not any(item.text == name_without_extension for item in
			           self.ids.nav_drawer.ids.navigation_menu.children[0].children):
				self.ids.nav_drawer.ids.navigation_menu.add_widget(MDNavigationDrawerItem(
					icon="book",
					text=name_without_extension,
					on_press=self.go_to_list_content
				))
	# back to lists
	def go_to_list_content(self, instance):
		index = len(self.ids.nav_drawer.ids.navigation_menu.children[0].children) - \
		        self.ids.nav_drawer.ids.navigation_menu.children[0].children.index(instance)
		# print(self.ids.nav_drawer.children[0].children[1].children[0].children[0].children[0].children[0])
		# for instance in self.ids.nav_drawer.ids.navigation_menu.children[0].children:
		#	print(instance.text)
		self.word_collection = Words_collection()
		self.card_view = Card_view()

		self.word_collection.name = f"words_collection_{index}"

		self.folder_path = rf'C:\Users\admin\PycharmProjects\smart_home\cards\{instance.text}.json'
		with open(self.folder_path, 'r', encoding='utf-8') as json_file:
			self.data = json.load(json_file)

		for key, value in self.data.items():
			self.word_collection.ids.words_list.add_widget(TwoLineListItem(
				text=f"{key}",
				secondary_text=f"{value}",
				on_press=(self.go_to_cards)
			))
		self.card_view.add_card(instance)

		# print(self.folder_path)
		Words_app.get_running_app().root.ids.sm.add_widget(self.word_collection)
		Words_app.get_running_app().root.ids.sm.current = f"words_collection_{index}"
		Words_app.get_running_app().root.ids.sm.transition.direction = "left"

	def go_to_cards(self, *args):
		app = Words_app.get_running_app()

		Words_app.get_running_app().root.ids.sm.current = "cards"

class Add_article_pop_up_window_content(MDFloatLayout):
	pass
# settings screen class
class Set(MDScreen):
	def set_org_lang(self):
		lang = ['da', 'en', 'ua']
		menu_items = [ {'text': f'{i}',
		                'on_release': lambda x=f"{i}": self.menu_item_selected(x),}
		               for i in lang]

		self.menu = MDDropdownMenu(
            caller=self.ids.org_lang,
            items = menu_items,
            width_mult=4
        )
		self.menu.open()
	def menu_item_selected(self, instance_menu_item):
		self.ids.org_lang.text = instance_menu_item

		self.menu.dismiss()

	def set_target_lang(self):
		lang = ['da', 'en', 'ua']
		menu_items = [{'text': f'{i}',
		               'on_release': lambda x=f"{i}": self.target_item_selected(x), }
		              for i in lang]

		self.menu = MDDropdownMenu(
			caller=self.ids.org_lang,
			items=menu_items,
			width_mult=4
		)
		self.menu.open()
	def target_item_selected(self, instance_menu_item):
		self.ids.target_lang.text = instance_menu_item

		self.menu.dismiss()

	def change_style(self):
		theme = ['dark', 'light']
		menu_items = [{'text': f'{i}',
		               'on_release': lambda x=f"{i}": self.theme_selected(x), }
		              for i in theme]

		self.menu = MDDropdownMenu(
			caller=self.ids.theme,
			items=menu_items,
			width_mult=4
		)
		self.menu.open()
	def theme_selected(self, instance_menu_item):
		self.ids.theme.text = instance_menu_item

		self.menu.dismiss()
		
		

		if self.ids.theme.text == 'dark':
			Words_app().theme_cls.theme_style = "Dark"
			#Words_app().theme_cls.primary_palette = "Orange"
			#Words_app().theme_cls.text_color = [1,1,1,1]  # Change to "Custom" to use your custom color
			#Words_app().theme_cls.primary_palette = 'Cyan'
		else:
			#Words_app().theme_cls.text_color = "Custom"  # Change to "Custom" to use your custom color
			#Words_app().theme_cls.primary_palette = 'Orange'
			Words_app().theme_cls.theme_style = "Light"
			#Words_app().theme_cls.primary_palette = "Green"

class Words_app(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Light"
		self.theme_cls.primary_palette = "Green"
		self.theme_cls.material_style = "M3"
		return Builder.load_string(KV)


Words_app().run()
