import os
import requests
from bs4 import BeautifulSoup

def extract_headings_and_content(url, file_number, output_folder="data"):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Fetch the HTML content
        response = requests.get(url)

        # Check for successful response
        if response.status_code == 200 and url.lower().endswith('.html'):
            if not os.path.exists(output_folder+'/html_data'):
              os.makedirs(output_folder+'/html_data')
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Define your extraction logic here for headings and their content
            extracted_data = []
            for heading_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                heading = heading_tag.text.strip()

                # Extracting content associated with the heading
                content = ""
                next_element = heading_tag.find_next_sibling()
                while next_element and next_element.name and next_element.name.startswith('h'):
                    break  # Stop if the next element is another heading
                while next_element and next_element.name and not next_element.name.startswith('h'):
                    content += str(next_element)  # Append content
                    next_element = next_element.find_next_sibling()

                extracted_data.append({'heading': heading, 'content': content})

            # Create the HTML structure for your extracted data
            html_content = f"<html><body><h1>Extracted Information</h1><ul>"
            for item in extracted_data:
                html_content += f"<li><strong>{item['heading']}</strong>: {item['content']}</li>"
            html_content += "</ul></body></html>"

            # Save the HTML file
            output_file = os.path.join(output_folder+'/html_data', f"html_file_{file_number}.html")
            with open(output_file, "w", encoding='utf-8') as file:
                file.write(html_content)

            return f"Extraction and saving successful for {url}. File saved as {output_file}"
        
        elif response.status_code == 200 and url.lower().endswith('.pdf'):
          if not os.path.exists(output_folder+'/pdf_data'):
              os.makedirs(output_folder+'/pdf_data')
          output_file = os.path.join(output_folder+'/pdf_data', f"pdf_file_{file_number}.pdf")
          with open(output_file,'wb') as file_:
            file_.write(response.content)
          return f"Extraction and saving successful for {url}. File saved as {output_file}"

        else:
            return f"Error fetching URL {url}: {response.status_code}"
    except Exception as e:
        return f"An error occurred for {url}: {str(e)}"

def word_wrap(string, n_chars=72):
    # Wrap a string at the next space after n_chars
    if len(string) < n_chars:
        return string
    else:
        return string[:n_chars].rsplit(' ', 1)[0] + '\n' + word_wrap(string[len(string[:n_chars].rsplit(' ', 1)[0])+1:], n_chars)


