import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
picked = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[picked]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    fruityice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityice_normalized)
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)


streamlit.text("What fruit would you like to add?")
fruit_choice = fruit_choice = streamlit.text_input('')
streamlit.text(f"Thanks for adding {fruit_choice}")
my_cur.execute(f"insert into fruit_load-list values('{fruit_choice}')")


