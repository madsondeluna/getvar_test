import pytest
import aiohttp
import asyncio
from src.api_getters import get_snp_summary, fetch_variation, fetch_all_variations

@pytest.mark.asyncio
async def test_get_snp_summary():
    snp_id = "rs123"
    result = await get_snp_summary(snp_id)
    assert "result" in result or "error" in result

@pytest.mark.asyncio
async def test_fetch_variation():
    async with aiohttp.ClientSession() as session:
        id = "rs123"
        headers = {"Content-Type": "application/json"}
        result = await fetch_variation(session, id, headers)
        assert "id" in result and (result["id"] == id or "error" in result)

@pytest.mark.asyncio
async def test_fetch_all_variations():
    ids = ["rs123", "rs456"]
    headers = {"Content-Type": "application/json"}
    results = await fetch_all_variations(ids, headers)
    assert len(results) == len(ids)
    for result in results:
        assert "id" in result and (result["id"] in ids or "error" in result)
