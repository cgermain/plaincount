import csv, sys
from datetime import datetime

TIME_FORMAT =  "%m-%d-%Y_%H-%M-%S"

def main(plain_parse_file):
	protein_mgf_list = []
	protein_dict = {}
	header = []

	gpm_filename = plain_parse_file.split("-")[0]

	with open(plain_parse_file, "rb") as in_file:
		csvreader = csv.reader(in_file, delimiter='\t')
		next(csvreader) #skip header
		for row in csvreader:
			# column 0 = filename
			# column 16 = protein
			# column 18 = gene
			protein = row[16] if row[18] == "None" else row[18]
			mgf_file = row[0]
			if protein not in protein_dict:
				protein_dict[protein] = {}
			if mgf_file not in protein_dict[protein]:
				protein_dict[protein][mgf_file] = 1
				if mgf_file not in header:
					header.append(mgf_file)
			else:
				protein_dict[protein][mgf_file]+=1

	timestamp = datetime.now().strftime(TIME_FORMAT)

	with open(gpm_filename+"_count_"+timestamp+".csv", 'wb') as out_file:
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