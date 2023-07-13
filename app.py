import os
import re
import time
from mtranslate import translate


def translate_russian_to_english(text):
    translation = translate(text, 'en', 'ru')
    return translation


def process_english_dat_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    ignore_list = [
        r'(?<!<)(Name|Description|Response_\w+|Message_\w+_Page_\w+)(?!>)',
        r'// Made in NPC Maker by BowieD',
        r'Character'
    ]

    # Preserve the HTML tags
    preserved_tags = {}
    preserved_counter = 0

    def preserve_tag(match):
        nonlocal preserved_counter
        tag = f"<TAG{preserved_counter}>"
        preserved_tags[tag] = match.group()
        preserved_counter += 1
        return tag

    # Exclude the words from translation using word boundaries (\b) and preserve the HTML tags
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, ignore_list)))
    content = re.sub(pattern, preserve_tag, content)

    # Translate the content with rate limiting
    translated_content = translate_russian_to_english(content)

    # Restore the preserved HTML tags
    for tag, preserved_tag in preserved_tags.items():
        translated_content = translated_content.replace(tag, preserved_tag)

    # Fix capitalization of "Name"
    translated_content = re.sub(r'(?<!<)\b(?:Name)\b(?!>)', 'Name', translated_content, flags=re.IGNORECASE)

    # Fix spaces in HTML tags
    translated_content = re.sub(r'\s*(?=[^<]*>)', '', translated_content)

    # Fix closing HTML tags
    translated_content = translated_content.replace("</Lor>", "</color>").replace("</Color>", "</color>")

    # Fix "comon" to "common"
    translated_content = translated_content.replace("comon", "common")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_content)

    print(f"Translated: {file_path}")

    # Add a delay of 0.5 seconds before processing the next file
    time.sleep(0.2)


def traverse_directory(directory):
    num_translated = 0  # Counter for translated files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower() == 'english.dat':
                file_path = os.path.join(root, file)
                process_english_dat_file(file_path)
                num_translated += 1

    print(f"Number of English.dat files translated: {num_translated}")

    #You need to add double blackslashesh when putting a directory in order for it to work: "C:\\Users\\Appdata\\Etc..."
root_directory = "C:\\Users\\Appdata\\Etc..."
traverse_directory(root_directory)
