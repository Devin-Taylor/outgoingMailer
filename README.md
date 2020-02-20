# WIP: outgoingMailer

An outgoing mailing server targeted at conferences that have to send responses to applicants but the contents of the email changes based on criteria specific to each applicant.

An example of this is - Did the applicant apply for a travel grant? If so, was the travel grant approved or denied?

### How it works

As much logic as possible has been abstracted into the config file. This file defines each section that needs to be added to the email, the conditional sections that need to exist in order for that section to be included, the conflicting sections that need to be checked before adding the section, and the dynamic fields and HTML tag parameters that need to be replaced on a applicant-by-applicant basis.

In order to work the following files need to be generated:

`<your_applicants_file>.csv`: Defines applicants names and emails addresses, and each of the categories that need to be responded to. The columns must correspond to the fields in the `config.yaml` file.

An example of this is as follows:

| idx | full_name | email | accept | travel_applied | travel |
|---|---|---|---|---|---|
| 1 | John Doe | john.doe@gmail.com | TRUE | TRUE | TRUE |
| 2 | Jane Doe | jane.doe@yahoo.com | TRUE | TRUE | FALSE |


`config.yaml`: defines the relationships between the different fields. Located in the root directory. These must correspond to columns in the `<your_applicants_file>.csv`.

An example of this is as follows:

```
admin:
    email: <outgoing-gmail-address>
    password: <email-account-password>
    email_subject: Your Amazing Conference
base_email:
    filename: base.html
    start_tag:
responses:
    accept:
        title:
        true_filename: accept.html
        false_filename: reject.html
        conditional: []
        conflict: []
        replacements:
            name:
                value: firstname
                params:
            response_link:
                value:
                params:
                    href: response_link
    travel:
        title: Travel Grant
        true_filename: travel_accepted.html
        false_filename: travel_rejected.html
        conditional: [travel_applied, accept]
        conflict: []
        replacements:
            bursary_name:
                value: bursary_name
                params:
            sponsor:
                value: sponsor
                params:
            response_link:
                value:
                params:
                    href: response_link
    talk:
        title: Talk
        true_filename: talk_accepted.html
        false_filename: talk_rejected.html
        conditional: [talk_applied, accept]
        conflict: []
        replacements:
            talk_length:
                value: talk_length
                params:
    poster:
        title: Poster
        true_filename: poster_accepted.html
        false_filename: poster_rejected.html
        conditional: [poster_applied, accept]
        conflict: []
        replacements:
    waitlist:
        title: Waitlist
        true_filename: waitlist.html
        false_filename:
        conditional: []
        conflict: [accept]
        replacements:
```

The following is a definition of the main fields:

| field      | sub field   | description                                                                           |
|------------|-------------|---------------------------------------------------------------------------------------|
| base_email | -           | template email with <html></html> and <body></body> tags                              |
|            | start_tag   | field tag to start inserting at. If blank, defaults to `body`                         |
| responses  | -           | all possible independent reponses                                                     |
|            | title       | title of section in email                                                             |
|            | conditional | boolean columns in csv file which this field is conditional on (i.e. need to be true) |
|            | conflicts   | boolean columns in csv file which this field conflicts with                           |
|            | replacements | list of fields and tag parameters to replace with dynamic variables |
|            | value | value to replace field value with (i.e. the value that will be displayed) |
|            | params | pairs of (param : replacement value) |


`responses/`: directory containing all `.html` files corresponding to the responses defined in `config.yaml`. Located in the root directory. Text must be contained within `<p></p>` braces and can contain any standard HTML formatting.


Example of `introduction.html`.
```
<p>
    Hi <var id="name">Name</var>!
    <br>
    <br>
    Thank you for applying to the Amazing Conference 2020.
</p>
```

### How to run

* edit recipient emails in `test_applications.csv`

* set gmail account details in config file

* run:

> python main.py -c "test_config.yaml" -r "test_responses" -a "test_applications.csv"
