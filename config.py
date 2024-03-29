#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os

class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword")
    LUIS_APP_ID = os.environ.get("LuisAPPId")
    LUIS_API_KEY = os.environ.get("LuisAPIKey")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("InstrumentationKey","cafe62a7-ac02-4e7e-b56d-5e10da4ecf1e")
