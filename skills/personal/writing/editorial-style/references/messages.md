# Messages

Emails, chat messages, and texts that Greg sends as himself. The decision
register still applies (mechanics, word list, no em dashes). This file adds
what a message needs that a document doesn't.

## Principles

- **Lead with the point or the ask.** The first sentence says why the reader
  is getting the message: the decision, the request, or the news. Context
  follows.
- **Keep the sender's intent.** When editing Greg's draft, change how it's
  said, not what it asks for, its position, or its commitments. Flag a change
  in meaning instead of making it.
- **Cut filler.** No "I hope this email finds you well", "just wanted to",
  "per my last email", or "please don't hesitate to reach out". Keep a short
  courtesy where it fits the relationship.
- **One message, one main ask.** A second unrelated request gets its own
  message or a clearly separate paragraph.
- **Make the ask answerable.** Say what you need, from whom, and by when:
  "Can you approve the change window by Thursday, December 3?"
- **Short paragraphs.** One to three sentences each. Use a list only for three
  or more parallel items, such as options or steps.
- **First person.** Write as Greg ("I", and "we" for a team he's part of).
- **Warm, not effusive.** Professional and friendly. No exclamation stacks,
  superlatives, or hype.
- **Explicit dates and times.** "Tuesday, December 1, at 2:00 PM CT", not
  "next Tuesday afternoon". Name the time zone for anyone outside Central time.
- **Descriptive links.** Link the document's title, never "here".

## By channel

| Channel | Shape |
| --- | --- |
| **Email** | A subject line that names the topic and the action ("Approval needed: December 1 change window"). A greeting, the point, supporting detail, the ask, and a short sign-off. |
| **Chat (Teams, Slack)** | No subject or greeting block. The point in the first line, detail after. Thread replies to the original message. |
| **Text message** | One or two sentences. The point and the ask only. |

## Delicate messages

When a message disagrees, declines, delivers bad news, or pushes back, state
the position plainly in the first two sentences, give the reason, and offer
the next step. Don't bury the position under apology or hedging, and don't
soften it so far that the reader misses it.

## Check

Run the checker on a plain-text draft before sending:

```bash
# Check an email draft as plain text.
python scripts/editorial_check.py draft.txt --text
```
