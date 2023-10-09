# VZ Frontend for Assistant Chatbot

## Deployment on Azure App Service

1. Add the repo to app service for CICD
2. Configuration for app startup: `python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0`. Refer to https://stackoverflow.com/questions/72442371/deploying-streamlit-app-in-azure-without-using-docker
3. Add to CORS '*'
4. Add PASSCODE, MESSAGE_ENDPOINT environment variables to Application Configuration.