import os
import yaml
import pandas as pd
from bs4 import BeautifulSoup
from Messages import Message
from Senders import SMTPSender

def main():
    # setup config
    with open("config.yaml", "r") as fd:
        config = yaml.load(fd, Loader=yaml.FullLoader)

    applications = pd.read_csv(config['infile'])

    messages = {
        "idx": [],
        "message": [],
        "sent": [],
        "reason": []
    }

    sender = SMTPSender(config['admin']['email'], config['admin']['password'], config['admin']['email_subject'])

    try:
        for idx in range(len(applications)):
            firstname = applications.iloc[idx, :]['full_name'].split(" ")[0]
            message = Message(os.path.join("responses", config['base_email']['filename']))
            message.add_component(os.path.join("responses", config['introduction']['filename']), level="H1", fields=["name"], values=[firstname])
            error = False
            reason = ""
            for response_type in config['responses'].keys():
                # check the following:
                #   1) response of interest is correct
                #   2) that all conditional fields are true
                #   3) that all conflicting fields are false
                if applications.iloc[idx, :][response_type]:
                    # flip booleans for all() otherwise all() of empty list is true which breaks the below check if it read `... and not ...`
                    conflicts = [not x for x in applications.iloc[idx, :][config['responses'][response_type]['conflict']].values]
                    conditionals = applications.iloc[idx, :][config['responses'][response_type]['conditional']].values
                    if all(conditionals) and all(conflicts):
                        message.add_component(os.path.join("responses", config['responses'][response_type]['filename']), config['responses'][response_type]['title'])
                    else:
                        error = True
                        reason = response_type
                        print(f"ID {applications.iloc[idx, :]['idx']}, response type {response_type} does not meet criteria to be sent, please review")
                        break

            if error:
                messages['idx'].append(applications.iloc[idx, :]['idx'])
                messages['message'].append("")
                messages['reason'].append(reason)
                messages['sent'].append(False)
            else:
                messages['idx'].append(applications.iloc[idx, :]['idx'])
                messages['message'].append(message.to_string())
                try:
                    sender.send_message(message.to_string(), applications.iloc[idx, :]['email'])
                    messages['sent'].append(True)
                    messages['reason'].append(reason)
                except Exception as e:
                    # bad practice but not sure what exception is thrown
                    messages['sent'].append(False)
                    reason = "Unable to send email " + str(e)
                    messages['reason'].append(reason)

        messages_df = pd.DataFrame(messages)
        messages_df.to_csv("completed.csv")
        print(messages_df)

    except Exception as e:
        # make sure we save progress if anything crashes
        messages_df = pd.DataFrame(messages)
        messages_df.to_csv("completed.csv")



if __name__ == "__main__":
    main()
