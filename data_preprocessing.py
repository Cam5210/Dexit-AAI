from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from urllib.parse import urlparse


def extract_base_url(url):
    # Use urlparse to parse the URL and extract the scheme and netloc
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def process_html_content(html_content, tags_to_remove, tags_to_change, new_tag):
    """
    Process HTML content to remove specified tags, change certain tags to a new tag,
    and extract content and deleted content.
    Parameters:
    - html_content: The HTML content as a string.
    - tags_to_remove: A list of tag names to remove from the HTML.
    - tags_to_change: A list of tag names to change to a new tag.
    - new_tag: The new tag name to replace tags_to_change with.
    Returns:
    - A tuple of two elements: final_content and deleted_final_content as strings.
    """
    soup = BeautifulSoup(html_content, 'html5lib')

    content = []
    deleted_content = []

    # Remove specified tags
    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):

            if tag.name is not None:  # Ensure tag has a name
                deleted_content.append('Deleted Tag: ' + str(tag))
                tag.decompose()
            else:
                # Debugging information
                print("Encountered an unusual tag:")
                print(tag_name)
                print("Encountered a tag with no name, skipping...")

    # Change specified tags to new_tag
    for tag_name in tags_to_change:
        for tag in soup.find_all(tag_name):
            deleted_content.append('Deleted Tag: ' + str(tag))
            tag.replace_with(soup.new_tag(new_tag, string=tag.text))
    # Extract remaining content
    for element in soup.recursiveChildGenerator():
        if element.name == 'a' or element.name == 'button':
            try:
                href = element.get('href')
                if href and not href.startswith('#'):
                    content.append(f"[Link  {href}]")
                else:
                    deleted_content.append(
                        'Deleted Link: ' + (str(href) if href else ''))
            except:
                pass
        elif element.name is None:
            text = element.strip()
            if text:
                content.append(text)

    # Prepare final content strings
    final_content = '\n'.join([item for item in content if item.strip()])
    deleted_final_content = '\n'.join(
        [item for item in deleted_content if item.strip()])
    return final_content, deleted_final_content


def clean_and_process_html_code(input_file_path, output_file_path, deleted_content_file_path, tags_to_remove, tags_to_change, new_tag):
    """
    Clean and process HTML code, saving the main content and deleted content to separate files.

    Parameters:
    - input_file_path: Path to the input HTML file.
    - output_file_path: Path to save the main content.
    - deleted_content_file_path: Path to save the deleted content.
    - tags_to_remove: List of tag names to remove from the HTML.
    - tags_to_change: List of tag names to change to a new tag.
    - new_tag: The new tag name to replace tags_to_change with.
    """
    # Read the HTML file
    with open(input_file_path, 'r') as file:
        html_content = file.read()

    # Process the HTML content
    # print('Processing HTML content...')
    final_content, deleted_final_content = process_html_content(
        html_content, tags_to_remove, tags_to_change, new_tag)

    # Save the main content to a file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_content)

    # Save the deleted (screened) content to a separate file
    with open(deleted_content_file_path, 'w', encoding='utf-8') as deleted_file:
        deleted_file.write(deleted_final_content)


def prepend_base_url_to_links(input_file_path, output_file_path, base_url):
    """
    Prepends the base URL to relative links in a text file.

    Parameters:
    - input_file_path: Path to the input text file.
    - output_file_path: Path to the output text file.
    - base_url: The base URL to prepend to relative links.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            if line.startswith("Link: /"):
                if input_file_path == 'cleaned_html_files/American Airlines_TOS_cleaned.txt':
                    # print(line)
                    pass
                # Prepend base URL to relative link
                line = "Link: " + base_url + line[6:]
                if input_file_path == 'cleaned_html_files/American Airlines_TOS_cleaned.txt':
                    # print("HERE")
                    # print(line)
                    pass

            output_file.write(line)


def main(links):
    """
    Main function to process HTML content and save the main content and deleted content to separate files.

    Parameters:
    - links: A list of lists containing company names, website URLs, and paths to HTML files.
    """
    cleaned_html_files = []
    output_file_paths_folder = 'cleaned_html_files'
    deleted_content_file_paths_folder = 'deleted_html_file_content'

    # Directories are created outside the loop to ensure they exist before processing files
    os.makedirs(output_file_paths_folder, exist_ok=True)
    os.makedirs(deleted_content_file_paths_folder, exist_ok=True)

    tos_dict = {}

    for link_info in links:
        company_name, website_url, html_file = link_info
        output_file_path = os.path.join(output_file_paths_folder, os.path.basename(
            html_file).replace('.html', '_cleaned.txt'))
        deleted_content_file_path = os.path.join(deleted_content_file_paths_folder, os.path.basename(
            html_file).replace('.html', '_deleted.txt'))

        clean_and_process_html_code(
            html_file, output_file_path, deleted_content_file_path,
            tags_to_remove=['link', 'style', 'script', 'meta',
                            'path', 'img', 'logo', 'noscript', 'iframe'],
            tags_to_change=['sup', 'sub'],
            new_tag='p')

        cleaned_html_files.append(output_file_path)

        # Construct the TOS dictionary entry for each company
        tos_dict[company_name] = {
            "website_url": website_url,
            "html_file": html_file,
            "cleaned_file_path": output_file_path,
            # Extract and include the base URL directly here
            "base_url": extract_base_url(website_url)

        }

    # Prepend base URL to links in cleaned HTML files and update TOS dictionary with extracted content and links
    for company_name, details in tos_dict.items():
        input_file_path = details['cleaned_file_path']
        output_file_path = f'cleaned_html_files_with_base_url/{company_name}_TOS_cleaned_with_base_url.txt'
        base_url = details['base_url']

        prepend_base_url_to_links(input_file_path, output_file_path, base_url)

    return tos_dict


links = [
    ["Facebook", "https://www.facebook.com/legal/terms",
        'html_files/Facebook_TOS.html'],
    ["American Express", "https://www.americanexpress.com/us/legal-disclosures/website-rules-and-regulations.html",
        'html_files/American Express_TOS.html'],
    ["Visa", "https://usa.visa.com/legal/global-privacy-notice.html",
        'html_files/Visa_TOS.html'],
    ["MasterCard", "https://www.mastercard.us/en-us/about-mastercard/what-we-do/terms-of-use.html",
        'html_files/MasterCard_TOS.html'],
    ["Discover", "https://www.discover.com/student-loans/help/interestonly?gcmpgn=1218_ZZ_srch_gsan_txt_2&srchQ=terms%20and%20conditions&srchC=internet_cm_fe", 'html_files/Discover_TOS.html'],
    ["Chase", "https://www.chase.com/digital/resources/terms-of-use",
        'html_files/Chase_TOS.html'],
    ["Delta Airlines", "https://www.delta.com/content/mobile/trip-extras/terms-and-conditions.html",
        'html_files/Delta Airlines_TOS.html'],
    ["American Airlines", "https://www.aa.com/i18n/customer-service/support/conditions-of-carriage.jsp",
        'html_files/American Airlines_TOS.html'],
    ["United Airlines", "https://www.united.com/ual/en/us/fly/contract-of-carriage.html",
        'html_files/United Airlines_TOS.html'],
    ["Southwest Airlines", "https://www.southwest.com/about-southwest/terms-and-conditions/",
        'html_files/Southwest Airlines_TOS.html'],
    ["Lufthansa", "https://www.lufthansa.com/us/en/terms-of-use",
        'html_files/Lufthansa_TOS.html'],
    ["British Airways", "https://www.britishairways.com/en-us/information/legal/british-airways/general-conditions-of-carriage",
        'html_files/British Airways_TOS.html'],
    ["Air France", "https://wwws.airfrance.us/information/legal",
        'html_files/Air France_TOS.html'],
    ["Emirates", "https://www.emirates.com/us/english/legal/terms-and-conditions/",
        'html_files/Emirates_TOS.html']
]

tos_dict = main(links)


tos_dict
