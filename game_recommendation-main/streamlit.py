import main
import streamlit as st # type: ignore
from bs4 import BeautifulSoup
import requests
import json

# Page title
st.markdown(f"<h1 style = 'font-weight: bold; text-transform: uppercase; opacity: 0.8; text-align: center;'>Game Recommendation App</h1>", unsafe_allow_html=True)

st.divider()

# Top Games
st.subheader("Top 5 Games Of All Time")

# Get top 5 games
top_5 = main.top_games().keys()

# Beautify game name
def beautify_name(name):
    new_name = ""
    for i in name:
        if i.isalnum() or i.isspace():
            new_name += i
        elif i == "'":
            pass
        else:
            pass
    
    new_name = new_name.replace(" ", "_")
    return new_name

# Get games SteamID using games name
def get_steamid(name):
    apps_list = requests.get(url='https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    data = json.loads(apps_list.text)

    appid = None
    for app in data['applist']['apps']:
        if app['name'] == name:
            appid = app['appid']
            break
    return appid

# Get image url, rating using games name
def app_data(name, appid):
    # get image url
    url = "https://store.steampowered.com/app/" + str(appid) + "/" + name + "/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    img = soup.find('img', {'class' : 'game_header_image_full'})
    img_source = str(img).split('"')[3]

    # -----------------------------------------------------------------------------------------

    # get rating value

    meta_string = soup.find('meta', itemprop='ratingValue') # return meta data containing rating value
    rating_value = str(meta_string).split('"')
    rating_value = rating_value[1]

    return img_source, rating_value, url

# converts text into href(hyperlink)
def steam_link(text, url):
    return f'<a href="{url}" style="color:inherit; text-decoration:none;">{text}</a>'


# display top 5 games in 5 parallel columns side by side
@st.cache_data
def display_top_games(_names_lst):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        image_url, rating, url = app_data(beautify_name(_names_lst[0]), get_steamid(_names_lst[0]))
        st.image(image_url)
        st.caption(steam_link(_names_lst[0], url), unsafe_allow_html=True)
    with col2:
        image_url, rating, url = app_data(beautify_name(_names_lst[1]), get_steamid(_names_lst[1]))
        st.image(image_url)
        st.caption(steam_link(_names_lst[1], url), unsafe_allow_html=True)
    with col3:
        image_url, rating, url = app_data(beautify_name(_names_lst[2]), get_steamid(_names_lst[2]))
        st.image(image_url)
        st.caption(steam_link(_names_lst[2], url), unsafe_allow_html=True)
    with col4:
        image_url, rating, url = app_data(beautify_name(_names_lst[3]), get_steamid(_names_lst[3]))
        st.image(image_url)
        st.caption(steam_link(_names_lst[3], url), unsafe_allow_html=True)
    with col5:
        image_url, rating, url = app_data(beautify_name(_names_lst[4]), get_steamid(_names_lst[4]))
        st.image(image_url)
        st.caption(steam_link(_names_lst[4], url), unsafe_allow_html=True)

display_top_games(top_5)

st.divider()

@st.cache_data
def display_game_header():
    # image_url, rating, steam_url = app_data(beautify_name(name), get_steamid(name))

    col1, col2, col3 = st.columns([3, 7, 1])
    with col1:
        st.markdown(f"<h1 style = 'font-size: 18px; opacity: 0.9; font-weight: bold;'></h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1 style = 'font-size: 18px; opacity: 0.9; font-weight: bold;'>Name</h1>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h1 style = 'font-size: 18px; opacity: 0.9; font-weight: bold;'>Rating</h1>", unsafe_allow_html=True)

def display_game(name):
    image_url, rating, steam_url = app_data(beautify_name(name), get_steamid(name))

    col1, col2, col3 = st.columns([3, 7, 1])
    with col1:
        st.image(image_url)
    with col2:
        st.caption(steam_link(name, steam_url), unsafe_allow_html=True)
    with col3:
        st.caption(rating)


st.markdown(f"<h1 style = 'font-size: 18px; opacity: 0.9; font-weight: bold;'>Search</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
qury = col1.text_input("", label_visibility="collapsed")
search = col2.button("Search...")
if search:
    st.write("Search Results For ---{}---".format(qury))
    lst_games_name = []
    try:
        lst_games_name = main.out(main.query(qury))

    except(ValueError):
        st.markdown(f"<h1 style = 'font-style: italic; color: red; font-size: 16px;'>This game does not exist in the database!!!</h1>", unsafe_allow_html=True)
    
    display_game_header()
    for i in lst_games_name:
        try:
            display_game(i)
        except(IndexError):
            pass
else:
    st.caption("Input Some Text To Start Searching...")







# st.write(main.out(main.query(qury)))
