# Get started
```zsh
brew install uv # if you do not have uv

uv venv
source .venv/bin/activate
uv add -r requirements.txt

uv run modal setup

# Generate a secure API key
API_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
echo "Generated API key: $API_KEY"
# Create the Modal secret with the API key
uv run modal secret create modal-hackathon-secrets API_KEY=$API_KEY
```

Then you copy the generate key from console output and provide it as a value to `VITE_MODAL_API_KEY=` in the frontend app's `.env`

To start the backend locally you run

```zsh
uv run modal serve main.py
```

and copy the api adress (in my case https://tegelstenen--modal-pdf-generator-generate-pdf-dev.modal.run) and add it as a secret to the front end's .env as `VITE_API_ENDPOINT=`

Add hugginface token too both locally and modal. Get it from huggingface website.
 
```zsh
touch .env

# Add your Hugging Face API token to the .env file
echo "HUGGINGFACEHUB_API_TOKEN=YOUR_SECRET" >> .env

# Or manually edit the .env file and add:
# HUGGINGFACEHUB_API_TOKEN=YOUR_SECRET
```