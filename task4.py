    if temp >= TEMP_THRESHOLD:
        if not relay_on:
            # Send alert every loop until /on arrives
            send_message(
                "ALERT: Temp {:.2f} C >= {} C!\n"
                "Send /on to activate relay.".format(temp, TEMP_THRESHOLD)
            )
        # If /on just received → alerts stop (relay_on is now True)

    else:
        # Temp back below threshold
        if relay_on:
            # Auto-OFF + one-time notice
            relay_on = False
            relay.value(0)
            send_message(
                "Auto-OFF: Temp {:.2f} C < {} C.\n"
                "Relay turned off automatically.".format(temp, TEMP_THRESHOLD)
            )

    time.sleep(POLL_INTERVAL)
