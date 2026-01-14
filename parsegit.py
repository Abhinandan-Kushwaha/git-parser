import aiohttp
import asyncio
import json

async def crawlPage(session, baseUrl, relPath):
    path = baseUrl + relPath

    async with session.get(path) as response:
        content = await response.text()

    index = content.find("\"tree\":{\"items\":[")
    if index == -1:
        return

    filesStr = content[index + len("\"tree\":{\"items\":[") - 1:]
    indexOfEnd = filesStr.find("]")
    filesArrayStr = filesStr[:indexOfEnd + 1]

    filesArray = json.loads(filesArrayStr)

    for item in filesArray:
        name = item.get("name")
        contentType = item.get("contentType")

        if contentType == "directory":
            if relPath == "":
                newRelPath = "/tree/master/" + name
            else:
                newRelPath = relPath + "/" + name

            await crawlPage(session, baseUrl, newRelPath)
        else:
            print(relPath.replace("/tree/master","") + "/" + name)


async def main():
    baseUrl = input("Enter Git url: ").strip()
    if(baseUrl.endswith("/")):
        baseUrl = baseUrl[0:-1]
    async with aiohttp.ClientSession() as session:
        await crawlPage(session, baseUrl, "")

asyncio.run(main())