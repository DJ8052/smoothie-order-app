# Import python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# User input
name_on_order = st.text_input('Name on Smoothie:')

st.write(
    'The name on your Smoothie will be:',
    name_on_order
)

# Create Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Pull fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME")) \
    .collect()

# Multi-select widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Only continue if ingredients selected
if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + ' '

    # Insert statement
    my_insert_stmt = f"""
        insert into smoothies.public.orders
        (ingredients, name_on_order)
        values
        ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success(
            f'Your Smoothie is ordered, {name_on_order}!',
            icon="✅"
        )

# New section to display smoothiefruit nutrition information
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

# Display JSON response
# st.text(smoothiefroot_response.json())

# Put JSON into a dataframe
sf_df = st.dataframe(
    data=smoothiefroot_response.json(),
    use_container_width=True
)
