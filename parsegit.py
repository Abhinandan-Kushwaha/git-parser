import aiohttp
import json
from fastapi import FastAPI, Query

app = FastAPI()

async def crawlPage(session, baseUrl, relPath, branch, results):
    path = baseUrl + relPath

    async with session.get(path) as response:
        content = await response.text()

    branchIndex = content.find("\"defaultBranch\":")
    if branchIndex == -1:
        return

    if branch == "":
        substring = content[branchIndex + 17: branchIndex + 57]
        comma = substring.find(",")
        branch = substring[:comma - 1]

    index = content.find("\"tree\":{\"items\":")
    if index == -1:
        return

    filesStr = content[index + len("\"tree\":{\"items\":"):]
    filesArrayStr = filesStr[:filesStr.find("]") + 1]
    files = json.loads(filesArrayStr)

    for item in files:
        name = item["name"]
        t = item["contentType"]

        if t == "directory":
            newRel = f"/tree/{branch}/{name}" if not relPath else f"{relPath}/{name}"
            await crawlPage(session, baseUrl, newRel, branch, results)

        elif t == "file" and name.endswith(".py"):
            results.append(relPath + "/" + name if relPath else name)

@app.get("/analyze")
async def analyze(repo_url: str = Query(...)):
    results = []
    async with aiohttp.ClientSession() as session:
        await crawlPage(session, repo_url.rstrip("/"), "", "", results)

    return {
        "repo": repo_url,
        "python_files": results
    }