import asyncio
import aiohttp

async def get_snp_summary(snp_id):
    """
    Fetches SNP summary information from the NCBI E-utilities API.

    Args:
        snp_id (str): The SNP ID to fetch the summary for.

    Returns:
        dict: A dictionary containing the SNP summary information or an error message.
    """
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={snp_id}&retmode=json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        return {"error": f"Failed to fetch data: {e}"}

async def fetch_variation(session, id, headers):
    """
    Fetches variation information from the Ensembl REST API.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        id (str): The variation ID to fetch.
        headers (dict): The headers to include in the request.

    Returns:
        dict: A dictionary containing the variation information or an error message.
    """
    url = f"https://rest.ensembl.org/variation/human/{id}"
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"id": id, "error": f"Failed to fetch data for {id}"}

async def fetch_all_variations(ids, headers):
    """
    Fetches variation information for multiple IDs from the Ensembl REST API.

    Args:
        ids (list): A list of variation IDs to fetch.
        headers (dict): The headers to include in the requests.

    Returns:
        list: A list of dictionaries containing the variation information or error messages.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_variation(session, id, headers) for id in ids]
        return await asyncio.gather(*tasks)
