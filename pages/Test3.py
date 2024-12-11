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
api_key = st.text_input("API Key", placeholder="Enter your AgentQL API Key", type="password")
url_to_scrape = st.text_input("URL to Scrape", "https://scrapeme.live/?s=fish&post_type=product")
query = st.text_area(
    "GraphQL Query (JSON format)", 
    """{
  "query": "{ products[] { product_name product_price(integer) } }"
}"""
)

params = st.text_area(
    "Params (JSON format, optional)",
    """{
  "wait_for": 0,
  "is_scroll_to_bottom_enabled": false,
  "mode": "fast",
  "is_screenshot_enabled": false
}"""
)

# Button to trigger the API request
if st.button("Scrape Data"):
    try:
        # Parse inputs
        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        query_json = json.loads(query)
        params_json = json.loads(params) if params.strip() else {}

        # Prepare the payload
        payload = {
            "query": query_json["query"],
            "url": url_to_scrape,
            "params": params_json
        }

        # Make the API request
        response = requests.post("https://api.agentql.com/v1/query-data", headers=headers, json=payload)

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
