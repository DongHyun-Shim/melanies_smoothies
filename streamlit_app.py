# Import python packages
import streamlit as st
import requests
import pandas
#from snowflake.snowpark.context import get_active_session    #SiS → SniS 로 바꿀때 수정
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My first Streamlit app. Yea! Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

#이제 주문자 이름 추가하기
name_on_order = st.text_input("Name on Smoothies")
st.write("The name on your smoothies will be:", name_on_order)



cnx = st.connection("snowflake")   #SiS → SniS 로 바꿀때 수정. 메세지를 상세히 읽자 ㅎㅎㅎㅎ
session = cnx.session() #SiS → SniS 로 바꿀때 수정
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))    #이게 여러 컬럼 셀렉트도 되는 구나..ㅋ
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert the Snowpark Dataframe to Pandas dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    , my_dataframe
    , max_selections=5
)

#위에서 멀티셀렉트된 것은 오브젝트 또는 데이터타입 LIST 다!
#LIST 는 DATAFRAME랑은 다르고, STRING하고도 다르다.
#st.write() , st.text() 를 쓸 수 있따.

if ingredients_list:
    #LIST를 STRING로 바꾸려면, 변수를 만들고 스트링이라고 인식시켜줘야 함
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('"""+ ingredients_string +"""','"""+ name_on_order +"""')
    """
    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    #if ingredients_string:      #선택한 결과 스트링이 있으면
    if time_to_insert:     #버튼을 클릭하면 - 으로 수정
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")















