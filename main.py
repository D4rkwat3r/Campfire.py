from asyncio import get_event_loop
from httpx import AsyncClient
from re import compile
from base64 import urlsafe_b64encode as b64
from os import urandom as rbytes
import camp
from random import choice

url_pattern = compile(r"oobCode=([A-z0-9_\-]+)")


def rstr(length: int) -> str:
    return b64(rbytes(length)).decode("utf-8").replace("=", "").replace("-", "").replace("_", "").lower()


async def secmail(action: str, **kwargs):
    async with AsyncClient() as client:
        params = dict(action=action, **kwargs)
        response = await client.get("https://www.1secmail.com/api/v1/",
                                    params=params)
        return response


async def generate():
    domains = [
        "1secmail.com",
        "1secmail.org",
        "1secmail.net",
        "wwjmp.com",
        "esiix.com",
        "oosln.com",
        "vddaz.com",
        "bheps.com",
        "dcctb.com"
    ]
    client = camp.Client()
    login, domain = f"{rstr(10)}@{choice(domains)}".split("@")
    print(f"Generated {login}@{domain} e-mail")
    fb_account = await client.create_account(f"{login}@{domain}", "123456q")
    print(f"Firebase account with e-mail {fb_account.email} created")
    await client.send_verification_code(fb_account.id_token)
    print(f"Verification code sent to {login}@{domain}")
    while True:
        messages = (await secmail("getMessages", login=login, domain=domain)).json()
        if len(messages) == 0:
            continue
        message_id = messages[0]["id"]
        print(f"Verification message received in {login}@{domain}")
        break
    read = (await secmail("readMessage", login=login, domain=domain, id=message_id)).json()
    url = url_pattern.search(read["body"]).groups(0)[0]
    print(f"Verification code in {login}@{domain}: {url}")
    await client.verify_account(url)
    print(f"Account {login}@{domain} verified")
    await client.login_by_token((await client.get_access_token(fb_account.refresh_token)).access_token)
    await client.change_name("Darkwater" + rstr(5))
    print(f"{login}@{domain} name changed")
    for i in range(10): await client.send_message(10, 2, 1, "Добрый вечер")
    print("Message Sent!")


async def polling(client: camp.Client):
    msgs = await client.get_chat_messages(10, 2, 1)
    last_msg = msgs[len(msgs) - 1].id
    while True:
        msgs = await client.get_chat_messages(10, 2, 1)
        if msgs[len(msgs) - 1].id == last_msg: continue
        print("Updated!")
        message = await client.send_message(10, 2, 1, f"Текст: {msgs[len(msgs) - 1].body.text}")
        last_msg = message["unitId"]
        print("Message sent!")


async def gen(proxy: str):
    try: await AsyncClient(proxies=proxy).get("http://deepthreads.ru:8000")
    except Exception as e: print(f"{proxy}: {e}")
    return
    try:
        await generate(proxy)
    except BadResponse as e:
        print(f"--- {proxy}: Error ({e.caused_by})")
    except APIException as e:
        print(f"--- {proxy}: API Exception ({e.message})")


async def main():
    key = "d0b9bdb1f592a46c6ea8a01e3e3112eb3e96aa561b9ed7a1e742550590ef"
    while True: await generate()


if __name__ == "__main__":
    get_event_loop().run_until_complete(main())
