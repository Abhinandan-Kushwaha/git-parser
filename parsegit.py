import aiohttp
import asyncio
import json

async def crawlPage(session, baseUrl, relPath, branch):
    path = baseUrl + relPath

    async with session.get(path) as response:
        content = await response.text()

    branchIndex = content.find("\"defaultBranch\":")

    if branchIndex == -1:
        return
    if branch == '':
        substring = content[branchIndex + 17 : branchIndex + 57] # considering max length of branch name to be 40
        nextCommaIndex = substring.find(",") # this(nextCommaIndex) is actually the length of the branch name
        if nextCommaIndex == -1:
            return
        branch = content[branchIndex + 17 : branchIndex + 17 + nextCommaIndex - 1]

    index = content.find("\"tree\":{\"items\":")
    if index == -1:
        return

    filesStr = content[index + len("\"tree\":{\"items\":"):]
    indexOfEnd = filesStr.find("]")
    filesArrayStr = filesStr[:indexOfEnd + 1]

    filesArray = json.loads(filesArrayStr)

    for item in filesArray:
        name = item.get("name")
        contentType = item.get("contentType")

        if contentType == "directory":
            if relPath == "":
                newRelPath = f"/tree/{branch}/" + name
            else:
                newRelPath = relPath + "/" + name

            await crawlPage(session, baseUrl, newRelPath, branch)
        else:
            path = baseUrl +f"/blob/{branch}"+ relPath + "/" + name
            if len(relPath)>0:
                print(relPath + "/" + name)
            else:
                print(name)
            async with session.get(path) as response:
                content = await response.text()
            if path.endswith(".py"):
                delimiter = "data-target=\"react-app.embeddedData\">"
                startIndex = content.find(delimiter) + len(delimiter)
                codeStr = content[startIndex:-1]
                endIndex = codeStr.find("</script>")
                codeStr = codeStr[0:endIndex]
                codeObj = json.loads(codeStr)
                code = codeObj.get("payload").get("blob").get("rawLines")
                print("_______________________________")
                print(f"Methods and classes in {name}-")
                for line in code:
                    x = line.strip()
                    if x.startswith("def "):
                        x=line.find("(")
                        # There is a corner case, if there is multiline string and If a line starts with def then it will also count.
                        y=line[4:x]
                        z=y.strip()
                        print("method: ",z)
                    elif x.startswith("Class"):
                        x=line.find("(")
                        y=line[5:x]
                        z=y.strip()
                        print("class: ",z)
                print("_______________________________")
                print("")
                print("")
            


async def main():
    baseUrl = input("Enter Git url: ").strip()
    if(baseUrl.endswith("/")):
        baseUrl = baseUrl[0:-1]
    branch = ''
    async with aiohttp.ClientSession() as session:
        await crawlPage(session, baseUrl, "", branch)

asyncio.run(main())