from google.cloud import secretmanager

def access_secret(secret_id, project_id, version_id: str = "latest"):

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    project = "open-weather-miroslav-kostov"
    secret_name = "open-weather-api-key"
    api_key = access_secret(secret_name, project)
    print("Retrieved API Key:", api_key)
    print(type(api_key))
