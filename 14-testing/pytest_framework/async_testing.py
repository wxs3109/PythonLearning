# Pytest Async Testing

import asyncio
import pytest

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

@pytest.mark.asyncio
async def test_fetch_data_success():
    assert await fetch_data() == "data"

@pytest.mark.asyncio
async def test_fetch_data_failure():
    with pytest.raises(Exception):
        await fetch_data()

asyncio.run(test_fetch_data_success())
asyncio.run(test_fetch_data_failure())