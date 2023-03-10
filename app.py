#!/usr/bin/env python
from http                           import HTTPStatus
#import asyncio
#from flask                          import Flask,request,Response
from aiohttp                        import web
from aiohttp.web                    import Request, Response, json_response
from botbuilder.core                import BotFrameworkAdapterSettings,ConversationState,MemoryStorage,UserState
from botbuilder.core.integration    import aiohttp_error_middleware
from botbuilder.schema              import Activity
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from botbuilder.applicationinsights.aiohttp import AiohttpTelemetryProcessor, bot_telemetry_middleware

from config import DefaultConfig
from dialogs import MainDialog, BookingDialog
from bots import DialogAndWelcomeBot

from adapter_with_error_handler import AdapterWithErrorHandler
from flight_booking_recognizer import FlightBookingRecognizer



#app = Flask(__name__)
#loop = asyncio.get_event_loop()

CONFIG              = DefaultConfig()
SETTINGS            = BotFrameworkAdapterSettings("","")
MEMORY              = MemoryStorage()
USER_STATE          = UserState(MEMORY)
CONVERSATION_STATE  = ConversationState(MEMORY)
ADAPTER             = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)
INSTRUMENTATION_KEY = CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY
TELEMETRY_CLIENT    = ApplicationInsightsTelemetryClient(INSTRUMENTATION_KEY, telemetry_processor=AiohttpTelemetryProcessor(), client_queue_size=1)

# Create dialogs and Bot
RECOGNIZER          = FlightBookingRecognizer(CONFIG)
BOOKING_DIALOG      = BookingDialog()
DIALOG              = MainDialog(RECOGNIZER, BOOKING_DIALOG, telemetry_client=TELEMETRY_CLIENT)
BOT                 = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG, TELEMETRY_CLIENT)


"""@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await BOT.on_turn(turncontext)

    task = loop.create_task(
        ADAPTER.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)


if __name__ == '__main__':
    app.run('localhost',3978)"""

# Listen for incoming requests on /api/messages.
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)


def init_func(argv):
    APP = web.Application(middlewares=[bot_telemetry_middleware, aiohttp_error_middleware])
    APP.router.add_post("/api/messages", messages)
    return APP


if __name__ == "__main__":
    APP = init_func(None)
    
    try:
        web.run_app(APP, host="0.0.0.0", port=CONFIG.PORT)
    except Exception as error:
        raise error
