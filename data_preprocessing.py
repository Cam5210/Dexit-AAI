from bs4 import BeautifulSoup


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
    soup = BeautifulSoup(html_content, 'html.parser')
    content = []
    deleted_content = []

    # Remove specified tags
    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):
            deleted_content.append('Deleted Tag: ' + str(tag))
            tag.decompose()

    # Change specified tags to new_tag
    for tag_name in tags_to_change:
        for tag in soup.find_all(tag_name):
            deleted_content.append('Deleted Tag: ' + str(tag))
            tag.replace_with(soup.new_tag(new_tag, string=tag.text))

    # Extract remaining content
    for element in soup.recursiveChildGenerator():
        if element.name == 'a':
            href = element.get('href')
            if href and not href.startswith('#'):
                content.append('Link: ' + href)
            else:
                deleted_content.append(
                    'Deleted Link: ' + (str(href) if href else ''))
        elif element.name is None:
            text = element.strip()
            if text:
                content.append('Text: ' + text)

    # Prepare final content strings
    final_content = '\n'.join([item for item in content if item.strip()])
    deleted_final_content = '\n'.join(
        [item for item in deleted_content if item.strip()])

    return final_content, deleted_final_content


def main(input_file_path, output_file_path, deleted_content_file_path):

    # Read the HTML file
    with open(input_file_path, 'r') as file:
        html_content = file.read()

    # Process the HTML content
    tags_to_remove = ['link', 'style', 'script', 'meta',
                      'path', 'img', 'logo', 'svg', 'noscript', 'iframe']
    tags_to_change = ['sup', 'sub']
    new_tag = 'p'
    final_content, deleted_final_content = process_html_content(
        html_content, tags_to_remove, tags_to_change, new_tag)

    # Save the main content to a file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_content)

    # Save the deleted (screened) content to a separate file
    with open(deleted_content_file_path, 'w', encoding='utf-8') as deleted_file:
        deleted_file.write(deleted_final_content)

# Example Usage of Main
# main('page1.html', 'output.txt', 'deleted_output.txt')
