import json
from os import listdir
from os.path import isdir, join, exists
from CDE_Model.cdedatabase import CDEDatabase, JSONCoder, MongoCoder
from CDE_Model.CustomModels import CurieTemperature, NeelTemperature

write_separate_file = False
delete_negative_records = True

output_data_path = r''
models = [CurieTemperature, NeelTemperature]

record_dirs = []

for contents in listdir(output_data_path):
    if isdir(join(output_data_path, contents)):
        record_dirs.append(contents)
counter = 0
negative_record_counter = 0
for record_dir in record_dirs:
    # print(f'{counter} / {len(record_dirs)}')
    counter += 1
    for model in models:
        model_name = model.__name__
        record_file = join(output_data_path, record_dir, (model_name + '.json'))

        if exists(
                record_file):
            with open(record_file) as f:
                records = json.load(f)
                negative_records = []

                for record in records:
                    # print(record)
                    raw_unit = records[record]['raw_units']
                    try:
                        # raw_value = float(records[record]['raw_value'].replace('−', '-'))
                        value = max(records[record]['value'])
                        # print(f'Value: {value}')
                        if value < 0 and raw_unit == 'K':
                            negative_record_counter += 1
                            print(
                                f'Negative Record Found In: {record_dir}: Value: {value}, Raw Value: {records[record]["raw_value"]} Unit: {raw_unit}, Model: {model_name}, Total Negative Records Found: {negative_record_counter}, Paper: {counter} / {len(record_dirs)}')
                            negative_records.append(record)
                    except ValueError as e:
                        print(f'Skipped record: {record} in file {record_file} because {e}')

            if delete_negative_records:
                if len(negative_records) > 0:
                    db_root = join(output_data_path, record_dir)
                    db = CDEDatabase(db_root, coder=JSONCoder())
                    db.delete(model, negative_records)

                    if write_separate_file:
                        for record in negative_records:
                            records.pop(record)
                        cleaned_record_file = join(output_data_path, record_dir, (model_name + '_data_cleaned.json'))
                        with open(cleaned_record_file, 'w') as f:
                            json.dump(records, f)
