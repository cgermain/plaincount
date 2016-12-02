import csv, sys
from collections import Counter

OUT_NAME = "protein_mgf_count.csv"

def main(plain_parse_file):
	protein_mgf_list = []
	protein_dict = {}
	header = []

	with open(plain_parse_file, 'rb') as in_file:
		csvreader = csv.reader(in_file, delimiter='\t')
		next(csvreader)
		for row in csvreader:
			protein_name = row[16]
			mgf_filename = row[0]
			if protein_name not in protein_dict:
				protein_dict[protein_name] = {}
			if mgf_filename not in protein_dict[protein_name]:
				protein_dict[protein_name][mgf_filename] = 1
				if mgf_filename not in header:
					header.append(mgf_filename)
			else:
				protein_dict[protein_name][mgf_filename]+=1

	with open(OUT_NAME, 'wb') as out_file:
		csvwriter = csv.writer(out_file)
		csvwriter.writerow(["Protein"]+header)
		for protein in protein_dict:
			line = [protein]
			for mgf in header:
				if mgf in protein_dict[protein]:
					line.append(str(protein_dict[protein][mgf]))
				else:
					line.append("")
			csvwriter.writerow(line)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Usage: python plaincount.py plain_parsed_file"