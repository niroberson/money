import csv
if __name__=="__main__":
    with open('nodes.csv', 'r', newline='\n') as read_file:
        with open('new_nodes.csv', 'w', newline='\n') as write_file:
            reader = csv.DictReader(read_file, delimiter='\t')
            filednames = ['id:id', 'name:label']
            writer = csv.DictWriter(write_file, fieldnames=filednames, delimiter='\t')
            writer.writeheader()
            for line in reader:
                name = '"' + line['name:label'] + '"'
                writer.writerow({'id:id':line['id:id'], 'name:label':name})


