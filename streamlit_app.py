import streamlit 
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗  Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔  Hard-Boiled Free-Range Egg')
streamlit.text('  🥑  Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

fruits_selected=streamlit.multiselect("Pick some Fruits:",list(my_fruit_list.index),['Orange','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
                      
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit choie')
  else:
    fruityvice_normalized=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
   streamlit.error()
  

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
streamlit.header('Fruit Load list contains')
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
    
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row=get_fruit_load_list()
  streamlit.dataframe(my_data_row)

def add_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
    return 'Thanks for adding' + new_fruit

    
fruit_choice = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=add_row_snowflake(fruit_choice)
   streamlit.text('Back from function')

streamlit.stop()
  
streamlit.write('The user entered ', fruit_choice)


streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")


