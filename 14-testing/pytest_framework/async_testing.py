# Pytest Async Testing

import asyncio
import pytest


async def fetch_data():
    await asyncio.sleep(1)
    return "data"

@pytest.mark.asyncio #
async def test_fetch_data():
    assert await fetch_data() == "data"



asyncio.run(test_fetch_data())