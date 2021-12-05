from app.main.helper.logger import logger


def get_secret(client, project_id, secret_id, version_id="latest"):
    try:
        # Build the resource name of the secret version.
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return payload
    except Exception as e:
        logger.error(e)


def add_secret(client, project_id, secret_id, payload):
    try:
        # Build the resource name of the parent secret.
        parent = client.secret_path(project_id, secret_id)

        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        payload = payload.encode("UTF-8")

        # Add the secret version.
        response = client.add_secret_version(
            request={"parent": parent, "payload": {"data": payload}}
        )
    except Exception as e:
        logger.error(e)
