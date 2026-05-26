def handle_commands(temp, hum):
    """
    Task 3 – process /status, /on, /off.
    Returns True if /on was received this cycle (used by Task 4 logic).
    """
    global relay_on, last_update_id
    on_received = False

    updates = get_updates()
    for update in updates:
        last_update_id = update["update_id"]
        msg  = update.get("message", {})
        text = msg.get("text", "").strip()

        if text == "/status":
            state = "ON" if relay_on else "OFF"
            send_message(
                "Temp: {:.2f} C\n"
                "Humidity: {:.2f} %\n"
                "Relay: {}".format(temp, hum, state)
            )

        elif text == "/on":
            relay_on = True
            relay.value(1)
            on_received = True
            send_message("Relay turned ON.")

        elif text == "/off":
            relay_on = False
            relay.value(0)
            send_message("Relay turned OFF.")

    return on_received

send_message("Hello from ESP32! Bot is online and ready.")  # <-- Task 2 evidence

# ─────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────
print("Starting main loop...")

while True:
    # ── Task 1: read sensor ──────────────
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum  = sensor.humidity()
        print("Temp: {:.2f} C  |  Humidity: {:.2f} %".format(temp, hum))
    except OSError as e:
        print("DHT read error:", e)
        time.sleep(POLL_INTERVAL)
        continue   # skip this cycle safely

    # ── Tasks 3 & 4: handle commands ─────
    on_received = handle_commands(temp, hum)
