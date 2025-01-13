from flask import Blueprint, render_template, request
import asyncio
from src.utils import extract_ids, extract_ref_alt, get_frequencies, process_vcf
from src.api_getters import get_snp_summary, fetch_all_variations

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    """
    Renders the home page.

    Returns:
        str: The rendered home page template.
    """
    return render_template('home.html')


@views.route('/consult', methods=['GET', 'POST'])
def consult():
    """
    Handles the consultation of VCF files.

    Returns:
        str: The rendered consultation page template with the processed VCF data.
    """
    if request.method == 'POST':
        upload_file = request.files.get('search')

        if not upload_file:
            return render_template('consult.html', error="Escolha um arquivo VCF")

        vcf_df = process_vcf(upload_file)
        showed_vcf = vcf_df.iloc[:500]
        table_html = showed_vcf.to_html(classes='table table-striped ', index=False, header=True)

        return render_template('consult.html', table_html=table_html)

    return render_template('consult.html')


@views.route('/anotation', methods=['GET', 'POST'])
def anotation():
    """
    Handles the annotation of VCF files.

    Returns:
        str: The rendered annotation page template with the annotated data.
    """
    data = []
    MIN_SHOW = 0
    MAX_SHOW = 25

    variation_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if request.method == 'POST':
        upload_file = request.files.get('search')

        if not upload_file:
            return render_template('search.html', error="Escolha um arquivo VCF")

        file_content = upload_file.read().decode('utf-8')

        ids = extract_ids(file_content)
        ref_alt = extract_ref_alt(file_content)

        showed_ids = ids[MIN_SHOW:MAX_SHOW]
        showed_ref_alt = ref_alt[MIN_SHOW:MAX_SHOW]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(fetch_all_variations(showed_ids, variation_headers))

        snp_data = []
        for snp_id in showed_ids:
            snp_id = ''.join(filter(str.isdigit, snp_id))
            snp_info = loop.run_until_complete(get_snp_summary(snp_id))
            snp_data.append(snp_info)

        studies = ['1000Genomes', 'ExAC', 'GnomAD', 'GnomAD_exomes', 'ALFA', 'OPMEDi']
        frequencies = get_frequencies(snp_data, studies)

        return render_template('search.html', data=data, frequencies=frequencies, ref_alt=showed_ref_alt)

    return render_template('search.html')
