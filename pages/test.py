import streamlit as st
import warnings

# Suppress the specific warning
warnings.filterwarnings("ignore", message='Field name "schema" in "FirecrawlApp.ExtractParams" shadows an attribute in parent "BaseModel"')

from firecrawl import FirecrawlApp

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

        # Initialize FirecrawlApp
        try:
            app = FirecrawlApp(api_key=api_key)

            # Scrape the website
            scrape_result = app.scrape_url(url, params={"formats": ["markdown", "html"]})

            if scrape_result.get("success"):
                st.success("Scraping successful!")

                # Extract and display content
                markdown_content = scrape_result.get("data", {}).get("markdown", "")
                html_content = scrape_result.get("data", {}).get("html", "")

                if markdown_content:
                    st.write("### Scraped Content (Markdown):")
                    st.markdown(markdown_content)
                elif html_content:
                    st.write("### Scraped Content (HTML):")
                    st.code(html_content, language="html")

                else:
                    st.warning("No relevant content was found on the page.")
            else:
                st.error(f"Scraping failed: {scrape_result.get('error', 'Unknown error')}")
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
