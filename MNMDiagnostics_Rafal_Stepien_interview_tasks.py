# #!bin/python3

from collections import Counter
import gzip


# ------------------------------- TASK 1 -------------------------------------------

def change_letters_size(input_string):
    """
    :param input_string: String to be changed
    :return: List with two strings
    """
    str_1, str_2 = '', ''
    for id, letter in enumerate(input_string):
        if id % 2 == 0:
            str_1 += letter.upper()
            str_2 += letter
        else:
            str_1 += letter
            str_2 += letter.upper()
    return [str_1, str_2]


print(change_letters_size("abcdef"))


# ------------------------------- TASK 2 -------------------------------------------

def get_number_of_redundant(input_string):
    """
    :param input_string: String to count occurrences in
    :return: number of letters appearing more than once in input_string
    """
    main = Counter(list(input_string.lower()))
    more_than_once = []
    for letter, occurrences in main.items():
        if occurrences > 1:
            more_than_once.append(letter)
    return len(more_than_once)


print(get_number_of_redundant('abba'))


# ------------------------------- TASK 3 -------------------------------------------

def subset_vcf(input_filename, output_filename):
    """
    :param input_filename: Input VCF file name
    :param output_filename: Output VCF file name
    :return: VCF file with location between 112204691 and 112247789 on chromosome 12
    """
    with gzip.open(input_filename, 'rb') as f:
        new_vcf = ''
        header = ''
        for line in f:
            line = line.decode("utf-8")
            if "#" not in line:
                line = line.split("\t")
                if (line[0] == "12") & (int(line[1]) >= 112204691) & (int(line[1]) <= 112247789):
                    new_vcf += '\t'.join(line) + "\n"
            else:
                header += line

    content = header + new_vcf
    save(output_filename, content)


def save(output_filename, content):
    """
    Saves file with specified filename
    """
    with open(output_filename, "w") as file:
        file.write(content)


subset_vcf('CPCT02220079.annotated.processed.vcf.gz', "chrom_12.vcf")

# ------------------------------- TASK 4 -------------------------------------------

# I assume that "For precise variants, END is POS + length of REF allele - 1, and the for imprecise variants the corresponding bestestimate."
# As written in VCF documentation : https://samtools.github.io/hts-specs/VCFv4.1.pdf

import matplotlib.pyplot as plt


def get_indel_length_histograms(input_filename):
    """
    :param filename: VCF input file name
    :return: Dictionary with chromosomes and their lengths
    """
    chromosomes = dict()
    with gzip.open(input_filename, 'rb') as f:
        for line in f:
            line = line.decode("utf-8").split("\t")
            if "#" not in line[0]:
                chromosomes.setdefault(line[0], [])
                chromosomes[line[0]].append(abs(len(line[3]) - len(line[4])) + 1)
    plot_chromosomes_distribution(chromosomes)


def plot_chromosomes_distribution(chromosomes):
    """
    :param chromosomes: Dictionary with chromosomes and their lengths
    :return: Plot with lengths distribution per chromosome
    """
    plt.style.use('fivethirtyeight')
    figure, axis = plt.subplots(5, 5)
    axis = axis.ravel()
    for n, (chromosome, lengths) in enumerate(chromosomes.items()):
        bins = list(range(1, max(lengths)))
        axis[n].hist(lengths, bins=bins, edgecolor="black")
        axis[n].set_yscale('log')
        axis[n].set_title("Chromosome {}".format(chromosome), fontsize=10)
        axis[n].tick_params(axis='both', which='major', labelsize=10)
    plt.title = "Polymorphisms length distribution per chromosome"
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.025, hspace=0.5)
    plt.show()


get_indel_length_histograms('CPCT02220079.annotated.processed.vcf.gz')


# ------------------------------- TASK 5 -------------------------------------------

def count_allele_frequency(filename):
    with gzip.open(filename, 'rb') as f:
        """
        :param filename: VCF file name
        :return: Number of heterozygotic variants with allele frequency < 0.01 and genotype 0/1
        """
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

# ------------------------------- TASK 6 -------------------------------------------

from collections import OrderedDict
from statistics import mean
import matplotlib.pyplot as plt
import pandas as pd


def plot_depth_of_coverage(input_filename):
    """

    Plots mean depth of coverage per chromosome

    :param input_filename: VCF input file name
    """
    chromosomes = OrderedDict()
    with gzip.open(input_filename, 'rb') as f:
        for line in f:
            line = line.decode("utf-8").split("\t")
            if "#" not in line[0]:
                if line[0].isnumeric():
                    chromosomes.setdefault(line[0], [])
                    chromosomes[line[0]].append(int(line[7].split("DP=")[1].split(";")[0]))

    chromosomes_names = list(chromosomes.keys())
    chromosomes_mean_depth = [round(mean(depths), 4) for depths in chromosomes.values()]
    plot_coverage_per_chromosome(chromosomes_names, chromosomes_mean_depth)
    save_to_csv(chromosomes_names, chromosomes_mean_depth,
                "/home/rafcio/MNM/MNMDiagnostics/Mean_depth_per_chromosome.csv")


def save_to_csv(names, depths, path):
    """
    Saves given lists to csv

    :param names: List of chromosome names/ID's
    :param depths: List of mean depth of coverage per chromosome
    :param path: Path to output file
    """
    data = pd.DataFrame(list(zip(names, depths)), columns=["Chromosome", "Mean depth coverage"])
    data.to_csv(path)


def plot_coverage_per_chromosome(names, depths):
    """
    :param names: List of chromosome names/ID's
    :param depths: List of mean depth of coverage per chromosome
    """
    plt.style.use('fivethirtyeight')
    plt.bar(names, depths, color="#2a2b2a")
    plt.title("Mean depth of coverage for polymorphisms in chromosome")
    plt.xlabel("Chromosome")
    plt.ylabel("Mean depth of coverage")
    plt.show()


plot_depth_of_coverage('CPCT02220079.annotated.processed.vcf.gz')


# ------------------------------- TASK 7 -------------------------------------------
# I assume that if one from {HIGH, LOW, MODERATE, MODIFIER} is present in INFO, then mutation has impact on protein


def count_impacts(input_filename):
    number_of_modifications = 0
    with gzip.open(input_filename, 'rb') as f:
        for line in f:
            line = line.decode("utf-8").split("\t")
            if "#" not in line[0]:
                if any(impact in line[7] for impact in ("MODIFIER", "LOW", "MODERATE", "HIGH")):
                    number_of_modifications += 1

    return number_of_modifications


print(count_impacts('CPCT02220079.annotated.processed.vcf.gz'))
