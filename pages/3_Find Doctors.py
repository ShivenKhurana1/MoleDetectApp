import streamlit as st
from geopy.geocoders import Nominatim
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from transformers import pipeline
import pytesseract
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

# Google Places API URL- Converts lat.lng into map data
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Google Geocoding API URL - converts text input into lat & lng
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Create a text input field for the location
location = st.sidebar.text_input("Enter your current location:")

# Search & Display nearby clinics
if location:
    # Parameters for the geocoding API request
    geocode_params = {
        "address": location,  # Location name
        "key": api_key,  # Your Google Places API key
    }

    # Send the geocoding API request
    geocode_response = requests.get(geocode_url, params=geocode_params)

    # Parse the geocoding response
    geocode_data = geocode_response.json()

    # Extract the latitude and longitude from the geocoding response
    lat = geocode_data['results'][0]['geometry']['location']['lat']
    lng = geocode_data['results'][0]['geometry']['location']['lng']

    # Parameters for the Places API request
    places_params = {
        "location": f"{lat},{lng}",  # Latitude and longitude
        "radius": 5000,  # Search radius in meters
        "type": "dermatologist",  # Type of place to search for
        "key": api_key,  # Your Google Places API key
    }

    # Send the Places API request
    places_response = requests.get(url, params=places_params)

    # Parse the Places response
    places_data = places_response.json()

    # Extract the clinic locations from the Places response
    clinics = pd.DataFrame([{
        'lat': result['geometry']['location']['lat'],
        'lon': result['geometry']['location']['lng'],
    } for result in places_data['results']])

    # Display the clinics on a map
    st.subheader("Dermatologists Near You")
    st.map(clinics)
