def send_message(text):
    """Task 2 – post a text message to the Telegram group."""
    try:
        resp = urequests.post(
            URL_SEND,
            json={"chat_id": CHAT_ID, "text": text}
        )
        resp.close()
    except Exception as e:
        print("send_message error:", e)


def get_updates():
    """Poll for new bot commands; return list of update dicts."""
    global last_update_id
    try:
        resp = urequests.get(
            URL_UPDATES + "?offset={}&timeout=1".format(last_update_id + 1)
        )
        data = resp.json()
        resp.close()
        return data.get("result", [])
    except Exception as e:
        print("get_updates error:", e)
        return []
