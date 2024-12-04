import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from pdfminer.high_level import extract_text
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

# Set up the sidebar
st.sidebar.title("ScholarScraper")
st.sidebar.markdown("### About the App")
st.sidebar.write("""
ScholarScraper is a powerful web scraping and data processing tool designed for researchers. 
It helps:
- Extract and filter conference attendee data.
- Scrape web pages and PDFs.
- Generate concise bios using AI models.
""")

# Settings in the sidebar
st.sidebar.title("Settings")
batch_size = st.sidebar.slider("Batch Size", min_value=10, max_value=500, value=200, step=10)
model = st.sidebar.selectbox("Choose AI Model", options=["gpt-3.5", "gpt-4"], index=1)
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Main app layout
st.title("ScholarScraper")
st.markdown("""
### A Researcher’s Tool for Efficient Data Processing and Web Scraping
Upload your files, choose tasks, and let ScholarScraper do the rest.
""")

# File upload
uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx"])
if uploaded_file:
    st.success("File uploaded successfully!")
    data = pd.read_excel(uploaded_file)
    st.write("Preview of the uploaded data:")
    st.dataframe(data)

    # Task selection
    task = st.selectbox(
        "Choose a Task",
        options=[
            "Filter and Save Batches",
            "Scrape Content from URLs",
            "Generate Bios for Conference Attendees"
        ],
    )

    if task == "Filter and Save Batches":
        st.subheader("Filter and Save Batches")
        num_batches = (len(data) + batch_size - 1) // batch_size
        st.write(f"The file will be split into {num_batches} batches of size {batch_size}.")
        for i in range(num_batches):
            start_row = i * batch_size
            end_row = start_row + batch_size
            batch_data = data.iloc[start_row:end_row]
            batch_file_name = f"batch_{i+1}.xlsx"
            batch_data.to_excel(batch_file_name, index=False)
            st.write(f"Batch {i+1} saved as {batch_file_name}.")

    elif task == "Scrape Content from URLs":
        st.subheader("Scrape Content from URLs")
        url_column = st.text_input("Column Name Containing URLs")
        if url_column and url_column in data.columns:
            st.write("Scraping content...")
            content = []
            for url in data[url_column].dropna():
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        page_text = soup.get_text(separator=" ", strip=True)
                        content.append(page_text[:500])  # Preview of content
                    else:
                        content.append(f"Failed to fetch URL: {url}")
                except Exception as e:
                    content.append(f"Error scraping {url}: {e}")
            data["Scraped Content"] = content
            st.write(data)
            st.download_button("Download Scraped Data", data.to_csv(index=False), "scraped_data.csv")

    elif task == "Generate Bios for Conference Attendees":
        st.subheader("Generate Bios for Conference Attendees")
        name_col = st.text_input("Column Name for Names")
        university_col = st.text_input("Column Name for Universities")
        if name_col and university_col and name_col in data.columns and university_col in data.columns:
            st.write("Generating bios using AI...")
            bios = []
            for i, row in data.iterrows():
                name = row[name_col]
                university = row[university_col]
                query = f"{name} {university}"
                try:
                    # Example API request to OpenAI (pseudo-code)
                    response = requests.post(
                        "https://api.openai.com/v1/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model,
                            "prompt": f"Generate a short bio for: {query}",
                            "max_tokens": 100,
                        }
                    )
                    bio = response.json()["choices"][0]["text"].strip()
                    bios.append(bio)
                except Exception as e:
                    bios.append(f"Error generating bio for {name}: {e}")
            data["Bio"] = bios
            st.write(data)
            st.download_button("Download Bios Data", data.to_csv(index=False), "bios_data.csv")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("ScholarScraper © 2024")
