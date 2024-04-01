import streamlit as st
from geopy.geocoders import Nominatim
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from transformers import pipeline
from PIL import Image
from dotenv import load_dotenv
import os


st.set_page_config(
    page_title="Skin Cancer",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('Moledetect: Dermafinder')

st.write('Currently Unavailable')
