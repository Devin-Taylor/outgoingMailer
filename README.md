# WIP: outgoingMailer

This application was specifically developed for the [IndabaX South Africa](https://indabax.co.za/) conference.

An outgoing mailing server targeted at conferences that have to send responses to applicants but the contents of the email changes based on criteria specific to each applicant.

An example of this is - Did the applicant apply for a travel grant? If so, was the travel grant approved or denied?

### How it works

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
    start_tag: startpt
introduction:
    title:
    filename: introduction.html
    replace_tags: [name]
    replace_values: [firstname]
responses:
    accept:
        title: Application Response
        true_filename: accept.html
        false_filename: reject.html
        conditional: []
        conflict: []
        replace_tags: [profession]
        replace_values: [profession]
    travel:
        title: Travel Grant
        true_filename: travel_accepted.html
        false_filename: travel_rejected.html
        conditional: [travel_applied, accept]
        conflict: []
        replace_tags: [sponsor]
        replace_values: [sponsor]
    talk:
        title: Talk
        true_filename: talk_accepted.html
        false_filename: talk_rejected.html
        conditional: [talk_applied, accept]
        conflict: []
        replace_tags: [talk_length]
        replace_values: [talk_length]
    poster:
        title: Poster
        true_filename: poster_accepted.html
        false_filename: poster_rejected.html
        conditional: [poster_applied, accept]
        conflict: []
        replace_tags: []
        replace_values: []
```

The following is a definition of the main fields:

| field      | sub field   | description                                                                           |
|------------|-------------|---------------------------------------------------------------------------------------|
| base_email | -           | template email with <html></html> and <body></body> tags                              |
|            | start_tag   | field tag to start inserting at. If blank, defaults to `body`                         |
| responses  | -           | all possible independent reponses                                                     |
|            | title       | title of section in email                                                             |
|            | conditional | boolean columns in csv file which this field is conditional on (i.e. need to be true) |

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
