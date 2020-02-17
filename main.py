import os
from dataclasses import asdict, dataclass  # python finally has structs 0.o
import logging

import pandas as pd
import yaml
from bs4 import BeautifulSoup

from Messages import Message
from Senders import SMTPSender

logging.basicConfig(level=logging.DEBUG)

def load_applicants(filename):
    return pd.read_csv(filename)

def load_config(filename):
    with open(filename, "r") as fd:
        config = yaml.load(fd, Loader=yaml.FullLoader)
    return config

@dataclass
class Tracking:
    idx: str=0
    message: str=""
    sent: bool=False
    reason: str=""

def main():
    logging.info("Loading config")
    config = load_config("config.yaml")
    logging.info("Loading applications")
    applications = load_applicants(config['infile'])

    sender = SMTPSender(config['admin']['email'], config['admin']['password'], config['admin']['email_subject'])
    tracking_messages = []

    try:
        for idx in range(len(applications)):
            error = False # flag used to determine if error occured while generating message
            message_tracker = Tracking(idx=applications.iloc[idx, :]['idx'])

            firstname = applications.iloc[idx, :]['full_name'].split(" ")[0]
            # build base email and introduction
            message = Message(os.path.join("responses", config['base_email']['filename']))
            message.add_component(os.path.join("responses", config['introduction']['filename']), config['introduction']['title'], level="H1", fields=["name"], values=[firstname])
            # check all components corresponding to an individual
            # 1) is the component set to true?
            # 2) if yes, are all conditional fields true?
            # 3) if yes, are all conflicting fields false?
            for response_type in config['responses'].keys():
                if applications.iloc[idx, :][response_type]:
                    # flip booleans for all() otherwise all() of empty list is true which breaks the below check if it read `... and not ...`
                    conflicts = [not x for x in applications.iloc[idx, :][config['responses'][response_type]['conflict']].values]
                    conditionals = applications.iloc[idx, :][config['responses'][response_type]['conditional']].values
                    if all(conditionals) and all(conflicts):
                        message.add_component(os.path.join("responses", config['responses'][response_type]['filename']), config['responses'][response_type]['title'])
                    else:
                        error = True
                        reason = response_type
                        logging.error("ID %s, response type %s does not meet criteria to be sent, please review", applications.iloc[idx, :]['idx'], response_type)
                        break

            if error:
                message_tracker.reason = reason
            else:
                message_tracker.message = message.to_string()
                try:
                    logging.debug("Sending message to %s: %s", applications.iloc[idx, :]['email'], message.to_string())
                    sender.send_message(message.to_string(), applications.iloc[idx, :]['email'])
                    message_tracker.sent = True
                except Exception as e:
                    # bad practice but not sure what exception is thrown
                    message_tracker.reason = "Unable to send email " + str(e)
            tracking_messages.append(asdict(message_tracker))

        tracking_messages_df = pd.DataFrame(tracking_messages)
        tracking_messages_df.to_csv("completed.csv")
        print(tracking_messages_df)

        sender.logout()

    except Exception as e:
        # make sure we save progress if anything crashes
        tracking_messages_df = pd.DataFrame(tracking_messages)
        tracking_messages_df.to_csv("completed.csv")



if __name__ == "__main__":
    main()
