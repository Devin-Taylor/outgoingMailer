import argparse
import logging
import os
import sys
from dataclasses import asdict, dataclass
from typing import Dict

import pandas as pd
import yaml

from mailer.Messages import Message
from mailer.Senders import SMTPSender

logging.basicConfig(level=logging.INFO)


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
    parser = argparse.ArgumentParser(
        description='Send out bulk emails to applicants.')
    parser.add_argument('-c', '--config', type=str,
                        help='path to configuration file')
    parser.add_argument('-r', '--responses', type=str,
                        help='path to responses directory')
    parser.add_argument('-a', '--applicants', type=str,
                        help='path to applicants csv file')

    return parser.parse_args(args_to_parse)


def main(args):

    logging.info("Loading config")
    config = load_config(args.config)

    logging.info("Loading applications")
    applications = load_applicants(args.applicants)

    sender = SMTPSender(config['admin']['email'], config['admin']
                        ['password'], config['admin']['email_subject'],
                        config['admin']['display_email'], config['admin']['display_name'])
    tracking_messages = []

    try:
        for idx in range(len(applications)):
            # just to save for review
            message_tracker = Tracking(idx=applications.iloc[idx, :]['idx'])

            # build base email and introduction
            message = Message(os.path.join(args.responses, config['base_email']['filename']), config['base_email']['start_tag'])

            # iterate over all applicants and build the remainder of their message
            for response_type in config['responses'].keys():
                foi = config['responses'][response_type] # extract field of interest of neatness
                # flip conflicts otherwise all(empty list) is true and breaks the below check
                conflicts = [not x for x in applications.iloc[idx, :][foi['conflict']].values]
                conditionals = applications.iloc[idx, :][foi['conditional']].values

                if all(conditionals) and all(conflicts): # read as "and not all(conflicts)"
                    if applications.iloc[idx, :][response_type]:
                        if foi['true_filename'] is not None:
                            message.add_component(os.path.join(args.responses, foi['true_filename']), foi['title'],
                                                    foi['replacements'], applications.iloc[idx, :].to_dict())
                    else:
                        if foi['false_filename'] is not None:
                            message.add_component(os.path.join(args.responses, foi['false_filename']), foi['title'],
                                                    foi['replacements'], applications.iloc[idx, :].to_dict())
                else:
                    logging.debug("ID %s, response type %s does not meet conditional criteria to be sent, leaving section off of email",
                                  applications.iloc[idx, :]['idx'], response_type)

            message_tracker.message = message.to_string()
            try:
                logging.debug("Sending message to %s: %s", applications.iloc[idx, :]['email'], message.to_string())
                sender.send_message(message.to_string(),
                                    applications.iloc[idx, :]['email'])
                message_tracker.sent = True
                logging.info("Message sent for idx=%s", applications.iloc[idx, :]['idx'])
            except Exception as e:
                # bad practice but not sure what exception is thrown when message could not be sent and not sure what else could come up
                # don't want to lose track of what happens
                message_tracker.reason = "Unable to send email " + repr(e)
                logging.error(repr(e))

            tracking_messages.append(asdict(message_tracker))
        sender.logout()

    except Exception as e:
        logging.error(repr(e))
        tracking_messages.append(asdict(message_tracker))

    tracking_messages_df = pd.DataFrame(tracking_messages)
    tracking_messages_df.to_csv("completed.csv")

if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    main(parsed_args)
