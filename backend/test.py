import requests
import xml.etree.ElementTree as ET

def fetch_forge_versions():
    url = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the XML from the response
        root = ET.fromstring(response.content)

        # Extract version information from the XML
        for version in root.find('versioning').findall('versions')[0].findall('version'):
            print("Version:", version.text)
    else:
        print("Failed to fetch data, status code:", response.status_code)

# Run the function
fetch_forge_versions()
