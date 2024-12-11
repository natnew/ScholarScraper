import streamlit as st
import requests

# Page title
st.title("LinkedIn Scraper")

# Description
st.markdown("""
Scrape LinkedIn profile information using the Multi-On API. Ensure your Multi-On API key is securely stored in Streamlit Cloud Secrets.
""")

# Input fields
url = st.text_input("Enter the LinkedIn profile URL to scrape:")
if st.button("Scrape"):
    if not url:
        st.error("Please enter a LinkedIn profile URL.")
    else:
        # Retrieve Multi-On API Key from Streamlit secrets
        try:
            api_key = st.secrets["MULTI_ON_API_KEY"]
        except KeyError:
            st.error("API Key not found in secrets. Please add it to Streamlit Cloud.")
            st.stop()

        # Multi-On API endpoint
        multi_on_endpoint = "https://api.multi-on.com/v1/scrape"

        # Request headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Payload
        payload = {
            "url": url,
            "actions": [
                {
                    "action": "scrape_profile",
                    "parameters": {}
                }
            ]
        }

        # Make the API request
        try:
            response = requests.post(multi_on_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse response
            data = response.json()
            if data.get("success"):
                st.success("Scraping successful!")

                # Display profile information
                profile_info = data.get("data", {}).get("profile", {})
                if profile_info:
                    st.write("### Scraped Profile Information")
                    for key, value in profile_info.items():
                        st.write(f"**{key.capitalize()}**: {value}")
                else:
                    st.warning("No profile information found.")
            else:
                st.error(f"Scraping failed: {data.get('error', 'Unknown error')}")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            st.error(f"An unexpected error occurred: {err}")

# Notes
st.markdown("""
---
**Notes:**
- The API key must be securely stored in Streamlit Cloud Secrets as `MULTI_ON_API_KEY`.
- This scraper works only for LinkedIn profiles with public access.
""")
