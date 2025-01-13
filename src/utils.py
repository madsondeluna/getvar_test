import pysam
import tempfile
import pandas as pd


def process_vcf(vcf_file):
    """
    Process a VCF file and extract relevant information.

    Args:
        vcf_file (str): Path to the VCF file.

    Returns:
        pd.DataFrame: DataFrame containing the extracted information.
    """
    vcf_data = []

    with pysam.VariantFile(vcf_file) as vcf_in:
        columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'DP', 'AF']

        for record in vcf_in:
            dp = record.info.get('DP', 'NA')  # 'NA' se não houver DP
            af = record.info.get('AF', ['NA'])[0]  # 'NA' se não houver AF

            row = [
                record.chrom,
                record.pos,
                record.id,
                record.ref,
                ','.join(str(alt) for alt in record.alts),
                record.qual,
                record.filter.keys() if record.filter else "PASS",
                dp,
                af,
            ]
            vcf_data.append(row)

    return pd.DataFrame(vcf_data, columns=columns)


def get_frequencies(snp_data, studies):
    """
    Extract frequencies of SNPs from the provided data.

    Args:
        snp_data (list): List of SNP data dictionaries.
        studies (list): List of study names to extract frequencies for.

    Returns:
        list: List of dictionaries containing frequencies for each SNP.
    """
    frequencies = []

    for snp_info in snp_data:
        if 'result' in snp_info:
            for snp_id, snp in snp_info['result'].items():
                if isinstance(snp, dict):
                    snp_frequencies = {}

                    global_mafs = snp.get('global_mafs', [])

                    for entry in global_mafs:
                        if isinstance(entry, dict):
                            study = entry.get('study')
                            freq = entry.get('freq')

                            if study in studies and freq:
                                snp_frequencies[study] = freq

                    if snp_frequencies:
                        frequencies.append(snp_frequencies)

    return frequencies


def extract_ids(file_content):
    """
    Extract variant IDs from the provided VCF file content.

    Args:
        file_content (str): Content of the VCF file.

    Returns:
        list: List of variant IDs.
    """
    variant_ids = []

    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".vcf") as temp_file:
            temp_file.write(file_content)
            temp_file.seek(0)  # Voltar ao início do arquivo

            vcf = pysam.VariantFile(temp_file.name)

            for record in vcf:
                if record.id:
                    variant_ids.append(record.id)

    except Exception as e:
        print(f"Erro ao processar o arquivo VCF: {e}")

    return variant_ids


def extract_ref_alt(file_content):
    """
    Extract reference and alternate alleles from the provided VCF file content.

    Args:
        file_content (str): Content of the VCF file.

    Returns:
        list: List of dictionaries containing reference and alternate alleles.
    """
    ref_alt_list = []

    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".vcf") as temp_file:
            temp_file.write(file_content)
            temp_file.seek(0)

            vcf = pysam.VariantFile(temp_file.name)

            for record in vcf:
                id = record.id
                if id and id.startswith("rs"):
                    chrom = record.chrom
                    ref = record.ref
                    alt = ','.join(str(a) for a in record.alts)
                    ref_alt_list.append({"chrom": chrom, "ref": ref, "alt": alt})

    except Exception as e:
        print(f"Erro ao processar o arquivo VCF: {e}")

    return ref_alt_list
