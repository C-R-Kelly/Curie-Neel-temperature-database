import chemdataextractor
from chemdataextractor.doc import Document
from chemdataextractor.errors import ReaderError

from os.path import join, splitext, exists
from os import listdir
import json

data_dir = r''
failed_dois = r''
output_directory = r''

loop_limit = 10
url_prefix = 'https://doi.org/'


def get_dois():
    failed_articles = []
    counter = 0

    articles = listdir(data_dir)
    for article in articles:
        print(f'reading article {article}, {counter} / {len(articles)}')
        if article.endswith('.xml') or article.endswith('.html'):
            dir = splitext(article)[0]
            output_path = join(
                output_directory,
                dir)
            output_path_file = join(output_path, 'doi.txt')
            if exists(output_path) and len(listdir(output_path)) > 0:
                if exists(output_path) and not exists(output_path_file):
                    try:
                        doc = Document.from_file(join(data_dir, article))
                        try:
                            doi = url_prefix + doc.metadata.doi
                            print(f'writing doi: {doi} to directory: {dir}')
                            with open(output_path_file, 'w', encoding='utf-8') as f:
                                f.write(doi)

                        except TypeError:
                            failed_articles.append(article)
                    except Exception as e:
                        failed_articles.append(article)

                elif exists(output_path_file):
                    print(f'doi detected for: {article}, skipping')
            else:
                print(f'no output records detected for {dir}, skipping')

            counter += 1
    return failed_articles


def save_failed_dois(dois):
    with open(failed_dois, 'w', encoding='utf-8') as f:
        for doi in dois:
            f.write(f'{doi}\n')


failed = get_dois()

save_failed_dois(failed)
