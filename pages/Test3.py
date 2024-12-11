import streamlit as st
import requests
import json

# Title and description of the app
st.title("AgentQL Data Scraping API Interface")
st.markdown(
    """
    Use this Streamlit app to interact with the [AgentQL Scraping Data API](https://docs.agentql.com/scraping/scraping-data-api).
    Enter the details below to scrape data using the API.
    """
)

# Input fields for API parameters
api_url = st.text_input("API Endpoint URL", "https://api.agentql.com/scrape")
url_to_scrape = st.text_input("URL to Scrape", "https://example.com")
fields = st.text_area(
    "Fields to Scrape (JSON format)", 
    """{
  "title": "title",
  "links": "a@href"
}"""
)

headers_input = st.text_area(
    "Headers (JSON format, optional)",
    """{
  "Authorization": "Bearer YOUR_API_KEY"
}"""
)

# Button to trigger the API request
if st.button("Scrape Data"):
    try:
        # Parse inputs
        headers = json.loads(headers_input) if headers_input.strip() else {}
        fields_json = json.loads(fields)

        # Prepare the payload
        payload = {
            "url": url_to_scrape,
            "fields": fields_json
        }

        # Make the API request
        response = requests.post(api_url, headers=headers, json=payload)

        # Display results
        if response.status_code == 200:
            st.success("Data scraped successfully!")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown(
    """
    ---
    Powered by [AgentQL](https://docs.agentql.com/scraping/scraping-data-api).
    """
)
