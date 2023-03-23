#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os

class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "d9d359df-4416-4937-86ee-51dbc2d56ca7")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword")
    LUIS_APP_ID = os.environ.get("LuisAPPId", "9660393f-a5bb-47ad-b0d5-4243c4380f58")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "f5f6103ab2534da097cd3d2101260b07")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "luischatbotzamant-authoring.cognitiveservices.azure.com/")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("InstrumentationKey", "9b99c404-7c88-4063-93fb-1db4df2e316e4")
