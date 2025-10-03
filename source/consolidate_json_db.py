import sys
import json
import os

sys.path.append(os.getcwd())

parent_json = r'E:\Programming\output_data_processed\curie_neel_database_data_processed.json'
parent_csv = r'E:\Programming\output_data_processed\curie_neel_database_processed.csv'
output_dir = r'E:\Programming\output_data_processed'

# parent_json = r'C:\PycharmProjects\PhD\CDE_Model\consolidate_json_db\curie_neel_database_data_cleaned.json'
# parent_csv = r'C:\PycharmProjects\PhD\CDE_Model\consolidate_json_db\curie_neel_database_data_cleaned.csv'
# output_dir = r'C:\PycharmProjects\PhD\CDE_Model\consolidate_json_db'

export_to_json = True
export_to_csv = True


def write_to_csv(database_dict):
    import csv
    flattened_data = []
    for record_id, record in database_dict.items():
        row = {'id': record_id}
        for key, value in record.items():
            if isinstance(value, list):
                row[key] = ', '.join(map(str, value))
            else:
                row[key] = value
        flattened_data.append(row)

    # Determine fieldnames (columns)
    fieldnames = sorted({k for row in flattened_data for k in row})

    # Write to CSV
    with open(parent_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)


def is_empty(directory):
    if not os.listdir(os.path.join(output_dir, directory)):
        return True
    else:
        return False


def is_dir(directory):
    if os.path.isdir(os.path.join(output_dir, directory)):
        return True
    else:
        return False


def get_data(directory):
    compound_data, curie_data, neel_data, doi = [], [], [], []
    if os.path.exists(os.path.join(output_dir, directory, 'Compound.json')):
        compound_path = os.path.join(output_dir, directory, 'Compound.json')
        with open(compound_path, 'r', ) as f:
            compound_data = json.load(f)

    if os.path.exists(os.path.join(output_dir, directory, 'CurieTemperature.json')):
        curie_path = os.path.join(output_dir, directory, 'CurieTemperature.json')
        with open(curie_path, 'r', ) as f:
            curie_data = json.load(f)

    if os.path.exists(os.path.join(output_dir, directory, 'NeelTemperature.json')):
        neel_path = os.path.join(output_dir, directory, 'NeelTemperature.json')
        with open(neel_path, 'r', ) as f:
            neel_data = json.load(f)

    if os.path.exists(os.path.join(output_dir, directory, 'doi.txt')):
        doi_path = os.path.join(output_dir, directory, 'doi.txt')
        with open(doi_path, 'r', encoding='utf-8') as f:
            doi = f.read()

    return compound_data, curie_data, neel_data, doi


if __name__ == '__main__':

    with open(parent_json, 'w') as database_json:
        parent_db_dict = {}
        parent_dict_starting_value = 1

        record_dirs = os.listdir(output_dir)
        for directory in record_dirs:
            if is_dir(directory) and not is_empty(directory):
                compound_data, curie_data, neel_data, doi = get_data(directory)

                print(f'Directory: {directory}, Curie: {curie_data}, Neel: {neel_data}, DOI: {doi}')
                if len(curie_data) > 0:
                    for c in curie_data:
                        curie_data[c]['names'] = compound_data[str(curie_data[c]['compound'])]['names']
                        curie_data[c]['_id'] = parent_dict_starting_value

                        del curie_data[c]['compound']
                        if 'error' in curie_data[c]:
                            del curie_data[c]['error']

                        curie_data[c]['doi'] = doi
                        parent_db_dict[str(parent_dict_starting_value)] = curie_data[c]
                        parent_dict_starting_value += 1

                if len(neel_data) > 0:

                    for n in neel_data:
                        neel_data[n]['names'] = compound_data[str(neel_data[n]['compound'])]['names']
                        neel_data[n]['_id'] = parent_dict_starting_value

                        del neel_data[n]['compound']
                        if 'error' in neel_data[n]:
                            del neel_data[n]['error']

                        neel_data[n]['doi'] = doi
                        parent_db_dict[str(parent_dict_starting_value)] = neel_data[n]
                        parent_dict_starting_value += 1

        if export_to_json:
            json.dump(parent_db_dict, database_json)

        if export_to_csv:
            write_to_csv(parent_db_dict)
