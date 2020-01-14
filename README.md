# Minimailer

Minimailer is a microservice that bridges your web / mobile application to SMTP servers or email delivery platforms.

## Quick Start

Minimailer is is easy to configure. Just put the following into `./etc/site.conf`:

```
[mailer:sendgrid1]
engine=sendgrid
sendgrid_api_key=SG.XXXXXX-tgw.XXXXXXXXXXXXXXXXXXXXXXXX
to=info@example.com
from=${from}
text_formatter=json
```

Run Minimailer:

	python3 ./minimailer.py -c ./etc/minimailer.conf

The microservice is now running and listening at `localhost:8080`

### Send email

In order to send an email from `john.doe@example.com` just send a REST call:

	$ curl -X POST 'http://localhost:8080/send/sendgrid1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"from": "john.doe@example.com:John Doe",
			"foo": "bar"
		}'

`info@example.com` will receive a plaintext email that looks like this:

```
from: john.doe@example.com:John Doe
foo: bar
```

## Included *Mailers*

- Sendgrid

just this one for now.

## Develop

Unit tests:

	python3 -m unittest
