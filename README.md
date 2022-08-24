# Campfire.py
Unofficial Campfire API on Python

## Login by email
```python3
import campfire

async def main():
  client = campfire.Client()
  await client.login("your email", "your password")
```

## Login by Firebase access token
```python3
import campfire

async def main():
  client = campfire.Client()
  await client.login_by_token("access token")
```

## Create new account
```python3
import campfire

async def main():
  client = campfire.Client()
  # Create account
  firebase_account = await client.create_account("email", "password")
  # Verify account
  await client.send_verification_code(firebase_acount.id_token)
  await client.verify_account("OOB code (sent to email) or verification link")
  # Configure account
  token_info = await client.get_access_token(firebase_account.refresh_token)
  await client.login_by_token(token_info.access_token)
  await client.change_name("name")
  await client.set_sex(campfire.SexType.MALE)
  await client.set_account_settings(hello_is_showed=True, hello_short_is_showed=True)
  # Now you can log in to this account through the app using email and password
```

## Echo bot for public chats (due to the fact that the application uses FCM to receive messages, event-based handlers are not supported)

```python3
import campfire
async def polling(client: Client):
  msgs = await client.get_chat_messages("fandom id", "chat id", 1) # 1 - type of the chat
  last_msg = msgs[len(msgs) - 1].id
  while True:
      msgs = await client.get_chat_messages(, 2, 1)
      if msgs[len(msgs) - 1].id == last_msg: continue
      print("Message received")
      message = await client.send_message(10, 2, 1, f"Message text is \"{msgs[len(msgs) - 1].body.text}\"")
      last_msg = message["unitId"]
      print("Reply sent!")

async def main():
  client = campfire.Client()
  await client.login("email", "password")
  await polling(client)
```

## Send custom request
```python3
import campfire
async def main():
  client = campfire.Client()
  request = campfire.APIRequest(name="RYourRequestName")
  # Add custom field (optional)
  request.field("fieldKey", "fieldValue")
  # Or
  request.fieldKey("fieldValue")
  # Change language (if not called, English is used)
  request.language(campfire.LanguageID.RUSSIAN)
  # Get JSON response (can also accept a custom implementation of CampfireAPI)
  response = await request(client.api)
  # Or
  response = await request.send(client.api)
  # Now you read response like a regular dict
```
