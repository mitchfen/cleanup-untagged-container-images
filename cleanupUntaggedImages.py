import json, os

CONTAINER_NAME = os.environ['CONTAINER_NAME']
USERNAME = os.environ['USERNAME']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

headers = " -H \"Accept: application/vnd.github+json\" -H \"Authorization: Bearer " + GITHUB_TOKEN + "\""
apiUrl = " https://api.github.com/users/" + USERNAME + "/packages/container/" + CONTAINER_NAME + "/versions"

command = "curl -s" + headers + apiUrl + " > temp.json"
os.system(command)

with open('temp.json') as f:
  contents = f.read()
response = json.loads(contents)
os.system("rm ./temp.json")

# TODO: if response.message = "Package not found." throw

taglessImages = []
for i in range(len(response)):
    tags = response[i]['metadata']['container']['tags']
    if (len(tags) == 0):
        taglessImages.append(response[i]['id'])
if (len(taglessImages) == 0):
    print("No untagged images to delete.")
else:
    apiUrl = " https://api.github.com/user/packages/container/" + CONTAINER_NAME + "/versions/"
    for i in range(len(taglessImages)):
        apiUrl = " https://api.github.com/users/" + USERNAME + "/packages/container/" + CONTAINER_NAME + "/versions/"
        id = str(taglessImages[i])
        apiUrl += id # append version to be deleted to the apiUrl
        command = "curl -s -X DELETE " + headers + apiUrl
        print("❌ Deleting " + id + "...", end=" ")
        os.system(command)
        print("done.")
    print("✅ Done!")
