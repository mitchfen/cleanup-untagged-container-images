import json, requests

def getUntaggedImageVersions(headers, username, containerName):
    apiUrl = " https://api.github.com/users/" + username + "/packages/container/" + containerName + "/versions"
    response = requests.get(apiUrl, headers=headers)

    if (response.status_code != 200 ):
        print("Status code was " + str(response.status_code))
        raise Exception(str(response.text))

    responseContent = json.loads(response.content)
    untaggedImageVersions = []
    for i in range(len(responseContent)):
        tags = responseContent[i]['metadata']['container']['tags']
        if (len(tags) == 0):
            untaggedImageVersions.append(responseContent[i]['id'])
    return untaggedImageVersions

def removeUntaggedImages(headers, username, containerName, untaggedImageVersions):
    for i in untaggedImageVersions:
        apiUrl = " https://api.github.com/users/" + USERNAME + "/packages/container/" + CONTAINER_NAME + "/versions/"
        apiUrl += str(i) # append version to be deleted
        print("❌ Deleting " + str(i) + "...", end=" ")
        requests.delete(apiUrl, headers=headers)
        print("done.")
    print("✅ All untagged images deleted.")

def main():
    CONTAINER_NAME = os.environ['CONTAINER_NAME']
    USERNAME = os.environ['USERNAME']
    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    headers = {'Authorization': 'Bearer ' + GITHUB_TOKEN}

    untaggedImageVersions = getUntaggedImageVersions(headers, USERNAME, CONTAINER_NAME)

    if (len(untaggedImageVersions) == 0):
        print("No untagged images to delete!")
        quit()

    removeUntaggedImages(headers, USERNAME, CONTAINER_NAME, untaggedImageVersions)

if __name__ == '__main__':
    main()
