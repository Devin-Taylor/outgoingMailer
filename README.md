# WIP: outgoingMailer

An outgoing mailing server targeted at conferences that have to send responses to applicants but the contents of the email changes based on criteria specific to each applicant.

An example of this is - Did the applicant apply for a travel grant? If so, was the travel grant approved or denied?

### How it works

`<your_applicants_file>.csv`: Defines applicants names and emails addresses, and each of the categories that need to be responded to.

An example of this is as follows:

| idx | full_name | email | accept | travel_applied | travel_granted | travel_denied |
|---|---|---|---|---|---|---|
| 1 | John Doe | john.doe@gmail.com | TRUE | TRUE | TRUE | FALSE |
| 2 | Jane Doe | jane.doe@yahoo.com | TRUE | TRUE | FALSE | TRUE |


`config.yaml`: defines the relationships between the different fields. Located in the root directory.

An example of this is as follows:

```
admin:
    email: <outgoing-gmail-address>
    password: <email-account-password>
    email_subject: Your Amazing Conference
infile: <path/to/your_applicants_file>.csv
base_email:
    title: Amazing Conference 2020
    filename: base.html
introduction:
    filename: introduction.html
responses:
    accept:
        title: Application Response
        filename: accept.html
        conditional: []
        conflict: []
    travel_granted:
        title: Travel Grant
        filename: travel_granted.html
        conditional: [travel_applied]
        conflict: [travel_denied]
    travel_denied:
        title: Travel Grant
        filename: travel_denied.html
        conditional: [travel_applied]
        conflict: [travel_granted]
```

`responses/`: directory containing all html files corresponding to the responses defined in `config.yaml`. Located in the root directory. Text must be contained within `<p></p>` braces and can contain any standard HTML formatting.
