#!/usr/bin/env python3
import argparse
import os
import subprocess
from Bio import SeqIO
import itertools
import pandas as pd

#!/usr/bin/env python3
import argparse
import os
import subprocess
from Bio import SeqIO
import itertools
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate Average Nucleotide Identity (ANI) across a pair of genomes.")
    parser.add_argument("--genomes-dir", dest="gd", required=True, help="Directory containing genome sequences in FASTA format")
    parser.add_argument("--output-dir", dest="od", required=True, help="Output directory")
    parser.add_argument("--formatdb-executable", dest="fd", required=True, help="Directory of BLAST formatdb executable file")
    parser.add_argument("--blastall-executable", dest="bl", required=True, help="Directory of blastall executable file")
    parser.add_argument('-n', '--num_threads', metavar='num_cpu', dest='n', type=int, default=3, help='specify the number of threads used by blast (default=3)')
    parser.add_argument('--clean', metavar='clean_blast_db_output', dest='c', nargs="?", const=True, default=False, help='redundant files created by this program will be removed if this argument is added')

    return parser.parse_args()



def split_genome(query_file, output_dir, chop_len=1020):
    with open(query_file, "r") as qr_file:
        for record in SeqIO.parse(qr_file, "fasta"):
            seq = str(record.seq)
            for cut_num, cut_seq in enumerate([seq[i:i + chop_len] for i in range(0, len(seq), chop_len)]):
                if len(cut_seq) >= 100:
                    sgm_id = f"{record.id}_{cut_num}"
                    split_output_file = os.path.join(output_dir, "split_output", f"{os.path.basename(query_file)}.split")
                    with open(split_output_file, "a") as split_file:
                        split_file.write(f">{sgm_id}\n{cut_seq}\n")

def run_makeblastdb(subject_file, output_dir):
    db_output_dir = os.path.join(output_dir, "db_output")
    if not os.path.exists(db_output_dir):
        os.makedirs(db_output_dir)

    db_output_file = os.path.join(db_output_dir, os.path.splitext(os.path.basename(subject_file))[0])

    subprocess.run(["makeblastdb", "-in", subject_file, "-dbtype", "nucl", "-out", db_output_file])

    return db_output_file

def run_blastall(query_file, db_output_file, output_dir, num_threads):
    blast_output_file = os.path.join(output_dir, "blast_output", f"{os.path.basename(query_file)}_{os.path.basename(db_output_file)}.blast")
    subprocess.run(["blastn", "-query", os.path.join(output_dir, "split_output", f"{os.path.basename(query_file)}.split"),
                    "-db", db_output_file, "-evalue", "1e-15", "-out", blast_output_file, "-outfmt", "6", "-task", "blastn", "-num_threads", str(num_threads)])
    return blast_output_file

def calculate_ani(blast_output_file):
    id_cut = 30
    cvg_cut = 70
    sum_id = 0
    count = 0
    qr_best = set()

    with open(blast_output_file, "r") as blast_file:
        for line in blast_file:
            fields = line.split()
            if float(fields[3]) < 100 or fields[0] in qr_best:
                continue
            qr_best.add(fields[0])
            if float(fields[2]) <= id_cut or (float(fields[3]) * 100 / 1020) < cvg_cut:
                continue
            sum_id += float(fields[2])
            count += 1

    ani = sum_id / count if count != 0 else -1

    return ani

def main():
    args = parse_args()

    split_output_dir = os.path.join(args.od, "split_output")
    blast_output_dir = os.path.join(args.od, "blast_output")

    for directory in [args.od, split_output_dir, blast_output_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    genome_files = [f for f in os.listdir(args.gd) if f.endswith(('.fasta', '.fna'))]
    genome_combinations = itertools.combinations(genome_files, 2)

    results_list = []

    for query_genome, subject_genome in genome_combinations:
        query_file = os.path.join(args.gd, query_genome)
        subject_file = os.path.join(args.gd, subject_genome)

        split_genome(query_file, args.od)
        db_output_file = run_makeblastdb(subject_file, args.od)
        blast_output_file = run_blastall(query_file, db_output_file, args.od)
        ani = calculate_ani(blast_output_file)

        result = {
            "Genome1": os.path.basename(query_file),
            "Genome2": os.path.basename(subject_file),
            "ANI": ani
        }

        results_list.append(result)

    df = pd.DataFrame(results_list)
    df.to_csv(os.path.join(args.od, "ani_results.csv"), index=False, sep='\t')
    # Clean up if specified
    if args.c:
        cleanup(args.od)

if __name__ == "__main__":
    main()
