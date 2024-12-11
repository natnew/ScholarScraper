import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit App Title
st.title("Professor and University Scraper")

# Instructions for the user
st.markdown(
    """
    Enter a URL of a webpage, and this app will scrape the names of professors
    and their associated universities. Ensure your API key is securely stored in Streamlit Cloud Secrets.
    """
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
            "formats": ["html"]
        }

        # Make the API request
        try:
            response = requests.post(firecrawl_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse response
            data = response.json()
            if data.get("success"):
                st.success("Scraping successful!")

                # Extract HTML content
                html_content = data.get("data", {}).get("html", "")
                if html_content:
                    # Use BeautifulSoup to parse and extract names and universities
                    soup = BeautifulSoup(html_content, "html.parser")
                    results = []

                    # Find specific elements containing names and universities (update selectors as needed)
                    for item in soup.find_all("li"):
                        text = item.get_text(strip=True)
                        if " – " in text:  # Assuming names and universities are separated by "–"
                            name, university = map(str.strip, text.split("–", 1))
                            results.append(f"{name} is affiliated with {university}.")

                    # Display the extracted information
                    if results:
                        st.write("### Scraped Professors and Universities")
                        for result in results:
                            st.write(result)
                    else:
                        st.warning("No names or universities found on the page.")
                else:
                    st.warning("No content found in the response.")
            else:
                st.error(f"Scraping failed: {data.get('error', 'Unknown error')}\nDetails: {data.get('details')}")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            st.error(f"An unexpected error occurred: {err}")

# Notes for the user
st.markdown(
    """
    ---
    **Notes:**
    - Ensure the API key is securely stored in Streamlit Cloud Secrets as `FIRECRAWL_API_KEY`.
    - Visit [FireCrawl Documentation](https://docs.firecrawl.dev/features/scrape) for more details.
    """
)
