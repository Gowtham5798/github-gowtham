from flask import Flask, request, render_template_string
import base64
import google.cloud.dlp
import os
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound
from typing import List



app = Flask(__name__)

def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Access a secret version in Google Cloud Secret Manager.

    Args:
    project_id: GCP project ID
    secret_id: ID of the secret to access
    version_id: Version of the secret (default is "latest")

    Returns:
    The payload of the secret version as a string.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        # Return the payload as a string.
        return response.payload.data.decode("UTF-8")
    except NotFound:
        print(f"Secret with ID '{secret_id}' not found.")
        return None
        
project_input = os.getenv('project_name','skipify-demo') #feting from environment variable
surrogate_input = os.getenv('surrogate_name','CC') #feting from environment variableCC
# project_input="skipify-demo"
# surrogate_input="CC"
secret_id_key="key_name" 
key_name = access_secret_version(project_input, secret_id_key) #fetching from secret manager
secret_id_wrap="wrapkey_name"
wrapkey_name = access_secret_version(project_input, secret_id_wrap) #fetching from secret manager

@app.route('/', methods=['GET', 'POST'])
def home():
    global key_name,wrapkey_name,project_input,surrogate_input
    message = ''
    if request.method == 'POST':
        sensitive_input = request.form['sensitive_input']
        encrypted = deidentify_with_deterministic(project_input,sensitive_input,["US_SOCIAL_SECURITY_NUMBER","CREDIT_CARD_NUMBER","PHONE_NUMBER","EMAIL_ADDRESS","CREDIT_CARD_TRACK_NUMBER"],surrogate_input,key_name,wrapkey_name)
        message = f'Encrypted value is {encrypted}'
    return render_template_string('''
        <html>
            <body>
                <form method="post">
                    <textarea id="w3review" name="sensitive_input" rows="10" cols="50">Sample JSON with sensitive data goes here</textarea><br><br>
                    Infotype Supported: "US_SOCIAL_SECURITY_NUMBER","CREDIT_CARD_NUMBER","PHONE_NUMBER","EMAIL_ADDRESS","CREDIT_CARD_TRACK_NUMBER"<br><br>
                    <input type="submit" value="Submit"/>
                </form>
                <p>{{ message }}</p>
            </body>
        </html>
    ''', message=message)
    
def deidentify_with_deterministic(
    project: str,
    input_str: str,
    info_types: List[str],
    surrogate_type: str = None,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """Deidentifies sensitive data in a string using deterministic encryption.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
        surrogate_type: The name of the surrogate custom info type to use. Only
            necessary if you want to reverse the deidentification process. Can
            be essentially any arbitrary string, as long as it doesn't appear
            in your dataset otherwise.
        key_name: The name of the Cloud KMS key used to encrypt ('wrap') the
            AES-256 key. Example:
            key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The encrypted ('wrapped') AES-256 key to use. This key
            should be encrypted using the Cloud KMS key specified by key_name.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct Deterministic encryption configuration dictionary
    crypto_replace_deterministic_config = {
        "crypto_key": {
            "kms_wrapped": {"wrapped_key": wrapped_key, "crypto_key_name": key_name}
        },
    }

    # Add surrogate type
    if surrogate_type:
        crypto_replace_deterministic_config["surrogate_info_type"] = {
            "name": surrogate_type
        }

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_deterministic_config": crypto_replace_deterministic_config
                    }
                }
            ]
        }
    }

    # Convert string to item
    item = {"value": input_str}

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print(response.item.value)
    encrypted = response.item.value
    return encrypted
    


if __name__ == '__main__':
    app.run(debug=False)
