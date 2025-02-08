import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import validators
import re

# Function to get phone number location
def trace_phone_number(phone):
    try:
        number = phonenumbers.parse(phone)
        location = geocoder.description_for_number(number, "en")
        service_provider = carrier.name_for_number(number, "en")
        return location, service_provider
    except:
        return None, None

# Function to get location from website URL
def trace_website_location(url):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        domain = re.sub(r"https?://(www\.)?", "", url).split('/')[0]
        location = geolocator.geocode(domain)
        return location.latitude, location.longitude if location else (None, None)
    except:
        return None, None

# Function to show map
def show_map(lat, lon, label="Location"):
    m = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon], tooltip=label).add_to(m)
    return st_folium(m, width=700, height=500)

# Streamlit UI
st.title("📍 Phone & Web Tracer App")

option = st.selectbox("Select what you want to trace:", ["Phone Number", "Website URL"])

if option == "Phone Number":
    phone = st.text_input("Enter Phone Number (with country code):", "+919876543210")
    if st.button("Trace"):
        location, provider = trace_phone_number(phone)
        if location:
            st.success(f"📌 Location: {location}")
            st.info(f"📡 Service Provider: {provider}")
            geolocator = Nominatim(user_agent="geoapiExercises")
            loc = geolocator.geocode(location)
            if loc:
                show_map(loc.latitude, loc.longitude)
        else:
            st.error("Invalid phone number")

elif option == "Website URL":
    url = st.text_input("Enter Website URL (e.g., https://www.google.com)")
    if st.button("Trace"):
        if validators.url(url):
            lat, lon = trace_website_location(url)
            if lat and lon:
                st.success(f"🌍 Location found: {lat}, {lon}")
                show_map(lat, lon)
            else:
                st.error("Could not fetch location.")
        else:
            st.error("Invalid URL. Please enter a valid website link.")

