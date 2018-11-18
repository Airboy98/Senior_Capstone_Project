from kivy.app  import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.properties  import ListProperty, ObjectProperty
from kivy.uix.listview import ListItemButton, ListItemLabel, CompositeListItem, ListView
from kivy.uix.button import Button
from random import shuffle
from functools import partial
from SQLite_test import *
import json
import requests

profile_table_setup()
my_list = select_all_profiles()
item_list = ObjectProperty()
global current_user
current_user=""

class ItemListButton(ListItemButton):
    pass


#instance is the last button added
class MyScreenManager(ScreenManager):
    added_buttons = ListProperty([])
    item_list = ObjectProperty()
    box2 = ObjectProperty(None)

    def __init__(self,*args, **kwargs):
      super().__init__(*args, **kwargs)
      for i in my_list:
          name = i
          self.make_buttons(name)
          
          
    def make_buttons(self, name):
        newbutton = Button(text=name, id = name)
        newbutton.bind(on_press = partial(lambda a:self.auth(name)))
        self.added_buttons.append(newbutton)

    def delete_buttons(self):
        global current_user
        for i in self.box2.children:
            if i.text==current_user:
                self.box2.remove_widget(i)
        delete_profile(current_user)

    def create(self,*args):
        self.current = "create_screen"

    def update_buttons(self):

        #self.box2.clear_widgets()
        #shuffle(self.added_buttons)
        add_user = Button(text="Add New Profile")
        add_user.bind(on_press = self.create)
        #self.box2.add_widget(add_user)
        for i in self.added_buttons:
            name = i.text
            print(i.text)
            if (name not in select_all_profiles()):
                create_profile(name)
        #for j in select_all_profiles():
         #   newbutton = Button(text=j, id = j)
          #  newbutton.bind(on_press = partial(lambda a:self.auth(j)))
           # self.box2.add_widget(newbutton)
            #self.added_buttons.append(newbutton)
        for j in self.added_buttons:
            name = j.text
            j.bind(on_press= partial(lambda a:self.auth(name)))
            self.box2.add_widget(j)
            
            
            
        self.added_buttons[:]=[]

    def auth(self,instance):
        self.transition.direction = "left"
        self.current = "menu_screen"
        global current_user
        current_user = instance
        self.ids.bannerbutton.text = "Welcome " + instance + "!"


    def search_item(self, barcode_number):
        if barcode_number.text != '':
            r = requests.get(r'https://api.barcodelookup.com/v2/products?barcode='+barcode_number.text+'&formatted=y&key=vwsib6fj958n3v9vtjt7sgtch7xclr')
            data = r.json()
            # displaying in json format
            item = data['products'][0]['product_name']
            # grabbing the brand property from the products array. Debug for more info
            self.ids.itemname.text = item
            print(item)
            print(barcode_number.text)
        else:
            print("no barcode entered")

    def get_date(self, month, day, year):
        if month.text == "Select Month" or day.text == "Select Day" or year.text == "Select Year":
            print("Invalid Expiration Date")
        else:
            date = month.text+"/"+day.text+"/"+year.text
            self.ids.expdate.text = date
            print(date)

    def search_recipes(self):
        #if a list item is selected
        if self.item_list.adapter.selection:
            selection = self.item_list.adapter.selection[0].text
            App_ID = 'cf938db6'
            APP_KEY = '91a43a29d2211953084fcca6b71b005b'
            r = requests.get('https://api.edamam.com/search?q='+selection +'&app_id='+App_ID+'&app_key='+APP_KEY)
            data = r.json()
            for i in data['hits']:
                print('*****************************')
                print('*****************************')
                data1 = i['recipe']
                dishName = data1['label']
                print('Recipe for '+dishName)
                for recipe in data1['ingredientLines']:
                    print(recipe)  
     

  
class GroceryLoggerApp(App):

    def build(self):
        self.title = "Gro-Log"
        return MyScreenManager()

GroceryLoggerApp().run()