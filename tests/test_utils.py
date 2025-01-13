import pytest
import tempfile
import pandas as pd
from src.utils import process_vcf, get_frequencies, extract_ids, extract_ref_alt

def test_process_vcf():
    vcf_content = """##fileformat=VCFv4.2
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       10177   rs367896724     A       AC      .       .       DP=100;AF=0.5
1       10352   rs555500075     T       TA      .       .       DP=200;AF=0.8
"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".vcf") as temp_file:
        temp_file.write(vcf_content)
        temp_file.seek(0)
        vcf_df = process_vcf(temp_file.name)

    assert isinstance(vcf_df, pd.DataFrame)
    assert vcf_df.shape == (2, 9)
    assert list(vcf_df.columns) == ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'DP', 'AF']
    assert vcf_df['CHROM'].tolist() == ['1', '1']
    assert vcf_df['POS'].tolist() == [10177, 10352]
    assert vcf_df['ID'].tolist() == ['rs367896724', 'rs555500075']
    assert vcf_df['REF'].tolist() == ['A', 'T']
    assert vcf_df['ALT'].tolist() == ['AC', 'TA']
    assert vcf_df['DP'].tolist() == [100, 200]
    assert vcf_df['AF'].tolist() == [0.5, 0.8]

def test_get_frequencies():
    snp_data = [
        {
            'result': {
                'rs123': {
                    'global_mafs': [
                        {'study': '1000Genomes', 'freq': 0.1},
                        {'study': 'ExAC', 'freq': 0.2}
                    ]
                }
            }
        },
        {
            'result': {
                'rs456': {
                    'global_mafs': [
                        {'study': 'GnomAD', 'freq': 0.3},
                        {'study': 'ALFA', 'freq': 0.4}
                    ]
                }
            }
        }
    ]
    studies = ['1000Genomes', 'ExAC', 'GnomAD', 'ALFA']
    frequencies = get_frequencies(snp_data, studies)

    assert isinstance(frequencies, list)
    assert len(frequencies) == 2
    assert frequencies[0] == {'1000Genomes': 0.1, 'ExAC': 0.2}
    assert frequencies[1] == {'GnomAD': 0.3, 'ALFA': 0.4}

def test_extract_ids():
    vcf_content = """##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       10177   rs367896724     A       AC      .       .       .
1       10352   rs555500075     T       TA      .       .       .
"""
    ids = extract_ids(vcf_content)

    assert isinstance(ids, list)
    assert len(ids) == 2
    assert ids == ['rs367896724', 'rs555500075']

def test_extract_ref_alt():
    vcf_content = """##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       10177   rs367896724     A       AC      .       .       .
1       10352   rs555500075     T       TA      .       .       .
"""
    ref_alt_list = extract_ref_alt(vcf_content)

    assert isinstance(ref_alt_list, list)
    assert len(ref_alt_list) == 2
    assert ref_alt_list[0] == {'chrom': '1', 'ref': 'A', 'alt': 'AC'}
    assert ref_alt_list[1] == {'chrom': '1', 'ref': 'T', 'alt': 'TA'}
