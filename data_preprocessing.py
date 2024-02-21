from bs4 import BeautifulSoup

# Read the HTML file
with open('page1.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize the lists to track content and deleted content
content = []
deleted_content = []


def remove_tag(soup, tag_names, deleted_content):
    for tag_name in tag_names:
        for tag in soup.find_all(tag_name):
            # Before decomposing, add a representation of the tag to deleted_content
            deleted_content.append('Deleted Tag: ' + str(tag))
            tag.decompose()
    return soup


# Specify the tags to remove
tags_to_remove = ['link', 'style', 'script', 'meta',
                  'path', 'img', 'logo', 'svg', 'noscript', 'iframe']
soup = remove_tag(soup, tags_to_remove, deleted_content)


# Change all sup and sub tags to p tags
def change_tag(soup, tag_names, new_tag, deleted_content):
    for tag_name in tag_names:
        for tag in soup.find_all(tag_name):
            # Before replacing the tag, add a representation of the tag to deleted_content
            deleted_content.append('Deleted Tag: ' + str(tag))
            tag.replace_with(soup.new_tag(new_tag, string=tag.text))
    return soup


soup = change_tag(soup, ['sup', 'sub'], 'p', deleted_content)

for element in soup.recursiveChildGenerator():
    if element.name == 'a':
        href = element.get('href')
        if href and not href.startswith('#'):
            content.append('Link: ' + href)
        else:
            # Add non-matching 'a' elements to deleted_content
            deleted_content.append(
                'Deleted Link: ' + str(href) if href else '')
    elif element.name is None:
        text = element.strip()
        if text:
            content.append('Text: ' + text)
        else:
            # Skip adding empty strings to deleted_content here as they were not actively removed
            pass

# Filter out blank lines and join the content with newline characters
final_content = '\n'.join([item for item in content if item.strip()])
deleted_final_content = '\n'.join(
    [item for item in deleted_content if item.strip()])

# Save the main content to a file
with open('output2.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(final_content)

# Save the deleted (screened) content to a separate file
with open('deleted_content2.txt', 'w', encoding='utf-8') as deleted_file:
    deleted_file.write(deleted_final_content)
