# WIP: outgoingMailer

This application was specifically developed for the [IndabaX South Africa](https://indabax.co.za/) conference.

An outgoing mailing server targeted at conferences that have to send responses to applicants but the contents of the email changes based on criteria specific to each applicant.

An example of this is - Did the applicant apply for a travel grant? If so, was the travel grant approved or denied?

### How it works

In order to work the following files need to be generated:

`<your_applicants_file>.csv`: Defines applicants names and emails addresses, and each of the categories that need to be responded to. The columns must correspond to the fields in the `config.yaml` file.

An example of this is as follows:

| idx | full_name | email | accept | travel_applied | travel_granted | travel_denied |
|---|---|---|---|---|---|---|
| 1 | John Doe | john.doe@gmail.com | TRUE | TRUE | TRUE | FALSE |
| 2 | Jane Doe | jane.doe@yahoo.com | TRUE | TRUE | FALSE | TRUE |


`config.yaml`: defines the relationships between the different fields. Located in the root directory. These must correspond to columns in the `<your_applicants_file>.csv`.

An example of this is as follows:

```
admin:
    email: <outgoing-gmail-address>
    password: <email-account-password>
    email_subject: Your Amazing Conference
infile: <path/to/your_applicants_file>.csv
base_email:
    filename: base.html
    start_tag: startpt
introduction:
    title: Amazing Conference 2020
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

The following in a definition of the main fields:

| field      | sub field   | description                                                                           |
|------------|-------------|---------------------------------------------------------------------------------------|
| base_email | -           | template email with <html></html> and <body></body> tags                              |
|            | start_tag   | field tag to start inserting at. If blank, defaults to `body`                         |
| responses  | -           | all possible independent reponses                                                     |
|            | title       | title of section in email                                                             |
|            | conditional | boolean columns in csv file which this field is conditional on (i.e. need to be true) |
|            | conflicts   | boolean columns in csv file which this field conflicts with if both true              |

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