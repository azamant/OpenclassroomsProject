#!/usr/bin/env python
import os

class DefaultConfig:
    """Configuration for the bot."""
    PORT                = 3978
    #APP_ID             = os.environ.get("MicrosoftAppId")
    #APP_PASSWORD       = os.environ.get("MicrosoftAppPassword")
    LUIS_APP_ID         = "9660393f-a5bb-47ad-b0d5-4243c4380f58"
    LUIS_API_KEY        = 'f5f6103ab2534da097cd3d2101260b07'
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME  = 'https://luischatbotzamant-authoring.cognitiveservices.azure.com/'
    APPINSIGHTS_INSTRUMENTATION_KEY = "9b99c404-7c88-4063-93fb-1db4df2e316e"
