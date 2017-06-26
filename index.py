#==============================================================================
# Unofficial Holiday Genie: Alexa skill that names a holiday given a date. 
#==============================================================================

from datetime import datetime
import random 

#----------- Holiday Data ------------#

holiday_data = [[[] for day in range(32)] for month in range(13)]
holiday_data[1][15] = ["Wikipedia Day"]
holiday_data[1][21] = ["National Hugging Day"]
holiday_data[1][28] = ["Data Privacy Day"]
holiday_data[2][17] = ["Random Acts of Kindness Day"]
holiday_data[2][22] = ["World Thinking Day"]
holiday_data[3][10] = ["Middle Name Pride Day"]
holiday_data[3][14] = ["Pi Day"]
holiday_data[4][1] = ["April Fools' Day"]
holiday_data[4][21] = ["National Tea Day"]
holiday_data[4][22] = ["Earth Day"]
holiday_data[4][25] = ["DNA Day"]
holiday_data[4][30] = ["Honesty Day"]
holiday_data[5][4] = ["Star Wars Day"]
holiday_data[5][18] = ["International Museum Day"]
holiday_data[5][25] = ["Towel Day"]
holiday_data[5][26] = ["National Paper Airplane Day"]
holiday_data[6][21] = ["Go Skateboarding Day"]
holiday_data[6][28] = ["CAPS LOCK DAY"]
holiday_data[7][6] = ["National Fried Chicken Day"]
holiday_data[7][17] = ["World Emoji Day"]
holiday_data[7][22] = ["Pi Approximation Day"]
holiday_data[9][13] = ["International Chocolate Day"]
holiday_data[9][19] = ["International Talk Like a Pirate Day"]
holiday_data[9][28] = ["Ask a Stupid Question Day"]
holiday_data[10][1] = ["National Pizza Month"]
holiday_data[10][21] = ["International Day of the Nacho"]
holiday_data[10][23] = ["Mole Day"]
holiday_data[11][17] = ["International Students' Day"]
holiday_data[12][14] = ["Monkey Day"]

#----------- Lambda function entry ------------#
def lambda_handler(event, context):
    # Check to make sure function was called from correct app ID
    if (event['session']['application']['applicationId'] !=
        "amzn1.ask.skill.694eb925-7c65-426c-a723-be2eb18bad32"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

#----------- Events Routing ------------#

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetHolidayIntent":
        return get_holiday(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid Intent")

#----------- Alexa Response Helpers ------------#

def build_speechlet_response(title, s_output, c_output, should_end_session, reprompt_text=""):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": s_output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": c_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_speechlet_ssml_response(title, s_output, c_output, should_end_session, reprompt_text=""):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": s_output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": c_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }
    
def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }

#----------- Program Logic ------------#

def get_holiday(intent):
    # Error check for slot existance
    if "value" not in intent["slots"]["Day"]:
        return get_invalid_date_response()

    date = intent["slots"]["Day"]["value"]

    # Error check for correct slot parsing
    try:
        date_stripped = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        return get_invalid_date_response()

    print date_stripped
    holidays = holiday_data[date_stripped.month][date_stripped.day]

    session_attributes = {}
    speech_output = ""
    card_output = ""
    card_title = "Unofficial Holiday Genie"
    reprompt_text = ""
    should_end_session = True
    
    if len(holidays) == 0:
        speech_output = "<speak>I don't know of any unofficial holidays on %s. " \
                        "Time to make one up!</speak>" \
                        % get_spoken_date(date_stripped)
        card_output = "I don't know of any unofficial holidays on %d/%d. " \
                        "Time to make one up!" \
                        % (date_stripped.month, date_stripped.day) 
    else: 
        output_base = "You can celebrate %s on " % random.choice(holidays)
        speech_output = "<speak>" + output_base + get_spoken_date(date_stripped) + "!</speak>"
        card_output = output_base + "%d/%d!" % (date_stripped.month, date_stripped.day)

    return build_response(session_attributes, build_speechlet_ssml_response(
        card_title, speech_output, card_output, should_end_session))

def get_spoken_date(d):
    return "<say-as interpret-as='date' format='md'>%d/%d</say-as>" % (d.month, d.day)

def get_welcome_response():
    session_attributes = {}
    card_title = "Unofficial Holiday Genie - Welcome"
    speech_output = "I am the Unofficial Holiday Genie! " \
                    "Give me a date and I will tell you what to celebrate! " \
                    "What date would you like to ask about?"
    reprompt_text = "Ask me what to celebrate today!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, should_end_session, reprompt_text))

def get_help_response():
    session_attributes = {}
    card_title = "Unofficial Holiday Genie - Help"
    speech_output = "I am the Unofficial Holiday Genie! " \
                    "You can ask me what holiday to celebrate on a given date. " \
                    "For example, you can ask me what to celebrate today."
    reprompt_text = "Ask me what to celebrate today!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, should_end_session, reprompt_text))

def get_invalid_date_response():
    session_attributes = {}
    card_title = "Unofficial Holiday Genie - Unrecognized Date"
    speech_output = "I'm sorry, I did not understand the date you specified. " \
                    "Please try again or specify a different date."
    reprompt_text = "Ask me what to celebrate today!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, should_end_session, reprompt_text))

def handle_session_end_request():
    card_title = "Unofficial Holiday Genie - Thanks"
    speech_output = "Thank you for using the Unofficial Holiday Genie skill. " \
                    "See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
