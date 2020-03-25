#!bin/python3

# ------------------------------- TASK 1 -------------------------------------------

# def change_letters_size(input_string):
    # """
    # :param input_string: String to be changed
    # :return: List with two strings
    # """
    # str_1, str_2 = '', ''
    # for id, letter in enumerate(input_string):
    #     if id % 2 == 0:
    #         str_1 += letter.upper()
    #         str_2 += letter
    #     else:
    #         str_1 += letter
    #         str_2 += letter.upper()
    # return [str_1, str_2]

# ------------------------------- TASK 2 -------------------------------------------

# from collections import Counter

# def get_number_of_redundant(input_string):
# 	"""
# 	:param input_string: String to count occurrences in
# 	:return: number of letters appearing more than once in input_string
# 	"""
#     main = Counter(list(input_string.lower()))
#     more_than_once = []
#     for letter, occurrences in main.items():
#     	if occurrences > 1:
#     		more_than_once.append(letter)
#     return len(more_than_once)


# if __name__ == "__main__":
#     print(change_letters_size("abcdef"))
#     print(get_number_of_redundant('abba'))


# ------------------------------- TASK 3 -------------------------------------------

# import gzip

# def subset_vcf(filename):
# 	with gzip.open(filename, 'rb') as f:
# 		new_vcf = ''
# 		header = ''
# 		for line in f:
# 			line = line.decode("utf-8")
# 			if "#" not in line:
# 				line = line.split("\t")
# 				if (line[0] == "12") & (int(line[1]) >= 112204691) & (int(line[1]) <= 112247789):
# 					new_vcf += '\t'.join(line) + "\n"
# 			else:
# 				header += line
# 	content = header+new_vcf
# 	save(filename="chrom_12.vcf", content=content)

# def save(filename, content):
# 	with open(filename, "w") as file:
# 		file.write(content)

# subset_vcf('CPCT02220079.annotated.processed.vcf.gz')

# ------------------------------- TASK 5 -------------------------------------------
import gzip

def count_allele_frequency(filename):
	with gzip.open(filename, 'rb') as f:
		counter = 0
		for line in f:
			line = line.decode("utf-8").split("\t")
			if ("#" not in line[0]):
				if line[6] == "PASS":
					genotype = line[9].split(":")[0]
					if genotype == "0/1":
						try:
							tmp = line[7].split("GoNLv5_AF=")[1]
							allele_frequency = tmp.split(";")[0]
						except IndexError:
							allele_frequency = 999
						if float(allele_frequency) < 0.01:
							counter += 1
	return counter


print(count_allele_frequency('CPCT02220079.annotated.processed.vcf.gz'))
				