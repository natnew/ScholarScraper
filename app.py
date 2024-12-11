import streamlit as st
import requests
import json

# Set up the Streamlit app
st.title("Professor and University Scraper")

# Instructions
st.markdown(
    """Enter a URL of a university webpage, and this app will scrape the names of professors 
    and their associated universities using the FireCrawl API. Please ensure your FireCrawl API 
    key is stored securely in Streamlit secrets."""
)

# Input field for the URL
url = st.text_input("Enter the URL to scrape:")

# Button to trigger scraping
if st.button("Scrape"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        # Retrieve the FireCrawl API key from Streamlit secrets
        api_key = st.secrets["FIRECRAWL_API_KEY"]
        
        # Set up the FireCrawl API endpoint
        firecrawl_endpoint = "https://api.firecrawl.dev/v1/scrape"

        # Configure the request payload
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "url": url,
            "selectors": {
                "professors": "CSS_SELECTOR_FOR_PROFESSOR_NAMES",  # Replace with the CSS selector
                "university": "CSS_SELECTOR_FOR_UNIVERSITY"        # Replace with the CSS selector
            }
        }

        # Make the API request
        try:
            response = requests.post(firecrawl_endpoint, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                professors = data.get("data", {}).get("professors", [])
                universities = data.get("data", {}).get("university", [])

                if professors and universities:
                    # Display results in a table
                    results = zip(professors, universities)
                    st.write("### Scraped Results")
                    st.table([{"Professor": p, "University": u} for p, u in results])
                else:
                    st.warning("No data found. Please check the selectors or the webpage.")
            else:
                st.error(f"Failed to scrape. Error: {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown(
    """---
    #### Notes:
    - Ensure you replace `CSS_SELECTOR_FOR_PROFESSOR_NAMES` and `CSS_SELECTOR_FOR_UNIVERSITY` 
      with appropriate CSS selectors for the webpage structure.
    - API key is securely stored in Streamlit secrets.
    - Visit [FireCrawl documentation](https://docs.firecrawl.dev/introduction) for more details.
    """
)
