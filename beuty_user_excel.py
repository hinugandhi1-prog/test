import requests
from bs4 import BeautifulSoup
import pandas as pd

# Input URL ---
url = input("Enter website URL: ")

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    data = []

    # Page Title
    title = soup.title.text.strip() if soup.title else "Not Found"
    data.append(["Title", title])

    # Meta Description
    meta = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta["content"].strip() if meta else "Not Found"
    data.append(["Meta Description", meta_desc])

    # Headings
    for heading in soup.find_all(["h1", "h2", "h3"]):
        data.append([heading.name.upper(), heading.text.strip()])

    # Paragraphs
    for para in soup.find_all("p"):
        data.append(["Paragraph", para.text.strip()])

    # Links
    for link in soup.find_all("a", href=True):
        data.append(["Link", link["href"]])

    # Images
    for img in soup.find_all("img", src=True):
        data.append(["Image", img["src"]])

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Tag Type", "Content"])

    # Save to Excel
    df.to_excel("website_data.xlsx", index=False)

    print("\n✅ Data extracted successfully!")
    print("📁 Saved as: website_data.xlsx")

else:
    print(f"❌ Failed to retrieve page. Status code: {response.status_code}")
