import argparse
import logging
import os
import sys
from dataclasses import asdict, dataclass
from typing import Dict

import pandas as pd
import yaml

from Messages import Message
from Senders import SMTPSender

# logging.basicConfig(level=logging.DEBUG)

def load_applicants(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)

def load_config(filename: str) -> Dict:
    with open(filename, "r") as fd:
        config = yaml.load(fd, Loader=yaml.FullLoader)
    return config

@dataclass
class Tracking:
    idx: str = ""
    message: str = ""
    sent: bool = False
    reason: str = ""

def parse_args(args_to_parse):
    parser = argparse.ArgumentParser(description='Send out bulk emails to applicants.')
    parser.add_argument('-c', '--config', type=str, help='path to configuration file')

    return parser.parse_args(args_to_parse)

def main(args):

    logging.info("Loading config")
    config = load_config(args.config)

    logging.info("Loading applications")
    applications = load_applicants(config['infile'])

    sender = SMTPSender(config['admin']['email'], config['admin']['password'], config['admin']['email_subject'])
    tracking_messages = []

    try:
        for idx in range(len(applications)):
            message_tracker = Tracking(idx=applications.iloc[idx, :]['idx'])

            firstname = applications.iloc[idx, :]['full_name'].strip().split(" ")[0]
            # build base email and introduction
            message = Message(os.path.join("responses", config['base_email']['filename']), config['base_email']['start_tag'])
            message.add_component(os.path.join("responses", config['introduction']['filename']), config['introduction']['title'], level="H1", fields=["name"], values=[firstname])
            # check all components corresponding to an individual
            # 1) is the component set to true?
            # 2) if yes, are all conditional fields true?
            # 3) if yes, are all conflicting fields false?
            for response_type in config['responses'].keys():
                # conflicts = [not x for x in applications.iloc[idx, :][config['responses'][response_type]['conflict']].values]
                conditionals = applications.iloc[idx, :][config['responses'][response_type]['conditional']].values
                if all(conditionals):
                    if applications.iloc[idx, :][response_type]:
                        message.add_component(os.path.join("responses", config['responses'][response_type]['true_filename']), config['responses'][response_type]['title'])
                    else:
                        message.add_component(os.path.join("responses", config['responses'][response_type]['false_filename']), config['responses'][response_type]['title'])
                else:
                    logging.debug("ID %s, response type %s does not meet conditional criteria to be sent, leaving section off of email", applications.iloc[idx, :]['idx'], response_type)

            message_tracker.message = message.to_string()
            try:
                logging.debug("Sending message to %s: %s", applications.iloc[idx, :]['email'], message.to_string())
                sender.send_message(message.to_string(), applications.iloc[idx, :]['email'])
                message_tracker.sent = True
            except Exception as e:
                # bad practice but not sure what exception is thrown
                message_tracker.reason = "Unable to send email " + repr(e)

            tracking_messages.append(asdict(message_tracker))

        tracking_messages_df = pd.DataFrame(tracking_messages)
        tracking_messages_df.to_csv("completed.csv")
        print(tracking_messages_df)

        sender.logout()

    except Exception as e:
        logging.error(repr(e))
        # make sure we save progress if anything crashes
        tracking_messages.append(asdict(message_tracker))
        tracking_messages_df = pd.DataFrame(tracking_messages)
        tracking_messages_df.to_csv("completed.csv")
        print(tracking_messages_df)



if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    main(parsed_args)
