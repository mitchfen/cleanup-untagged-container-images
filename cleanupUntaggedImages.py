import os, json, requests, sys

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
        apiUrl = " https://api.github.com/users/" + username + "/packages/container/" + containerName + "/versions/"
        apiUrl += str(i) # append version to be deleted
        print("❌ Deleting " + str(i) + "...", end=" ")
        response = requests.delete(apiUrl, headers=headers)
        if (response.status_code != 204):
            print(f"Error deleting version {i}: {response.status_code} {response.text}")
            raise Exception(f"Failed to delete version {i}")
        print("done.")
    print("✅ All untagged images deleted.")

def main():
    try:
        USERNAME = os.environ['USERNAME']
        CONTAINER_NAME = os.environ['CONTAINER_NAME']
        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    except KeyError as e:
        print(f"Error: Missing required environment variable: {e}")
        sys.exit(1)

    headers = {'Authorization': 'Bearer ' + GITHUB_TOKEN}

    try:
        untaggedImageVersions = getUntaggedImageVersions(headers, USERNAME, CONTAINER_NAME)

        if (len(untaggedImageVersions) == 0):
            print("No untagged images to delete!")
            sys.exit(0)

        removeUntaggedImages(headers, USERNAME, CONTAINER_NAME, untaggedImageVersions)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
