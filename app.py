import streamlit as st
import requests



# Set the page configuration
st.set_page_config(
    page_title="Professor and University Scraper",  # Title of the tab in the browser
    page_icon="📊",                 # An optional emoji or icon
    layout="centered"                   # Optional layout setting
)

# Streamlit App Title
st.title("Professor and University Scraper")

# Instructions for the user
st.markdown(
    """Enter a URL of a webpage, and this app will scrape the content using the FireCrawl API. Ensure your API key is securely stored in Streamlit Cloud Secrets."""
)

# Input for the URL
url = st.text_input("Enter the URL to scrape:")

# Button to trigger scraping
if st.button("Scrape"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        # Retrieve FireCrawl API Key from Streamlit secrets
        try:
            api_key = st.secrets["FIRECRAWL_API_KEY"]
        except KeyError:
            st.error("API Key not found in secrets. Please add it to Streamlit Cloud.")
            st.stop()

        # FireCrawl API endpoint
        firecrawl_endpoint = "https://api.firecrawl.dev/v1/scrape"

        # Request headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Payload structure
        payload = {
            "url": url,
            "formats": ["markdown", "html"]  # Adjust formats as needed
        }

        # Make the API request
        try:
            response = requests.post(firecrawl_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse response
            data = response.json()
            if data.get("success"):
                st.success("Scraping successful!")
                st.json(data)  # Display scraped data
            else:
                st.error(f"Scraping failed: {data.get('error', 'Unknown error')}\nDetails: {data.get('details')}" )
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            st.error(f"An unexpected error occurred: {err}")

# Notes for the user
st.markdown(
    """---
    **Notes:**
    - Ensure the API key is securely stored in Streamlit Cloud Secrets as `FIRECRAWL_API_KEY`.
    - The FireCrawl API expects a valid URL and formats as part of the payload.
    - Visit [FireCrawl Documentation](https://docs.firecrawl.dev/features/scrape) for more details.
    """
)
