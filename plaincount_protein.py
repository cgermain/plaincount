import csv, sys, re, os
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

def main(plain_parse_file):
	protein_mgf_list = []
	protein_dict = {}
	header = []

	base_directory = os.path.split(plain_parse_file)[0]
	gpm_filename = os.path.split(plain_parse_file)[1].split("-pep-merged.txt")[0]

	with open(plain_parse_file, "rb") as in_file:
		csvreader = csv.reader(in_file, delimiter='\t')
		next(csvreader) #skip header
		for row in csvreader:
			# column 0 = filename
			# column 16 = protein
			# column 18 = gene
			protein = row[16]
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

	out_filename = os.path.join(base_directory, gpm_filename+"_protein_count_"+timestamp+".csv")

	with open(out_filename, 'wb') as out_file:
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

	print "Wrote out: " + out_filename

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1].endswith("pep-merged.txt"):
		main(sys.argv[1])
	else:
		print "Usage: python plaincount.py plain_parse_file"
		print "Note: Plain parse file ends with -pep-merged.txt"
	raw_input("press ENTER to exit")