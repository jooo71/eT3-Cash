import vonage

# client = vonage.Client(key="0606299a", secret="C3Ku7R8yGAn9uzRl")
# sms = vonage.Sms(client)


# responseData = sms.send_message(
#     {
#         "from": "Vonage APIs",
#         "to": "201003793415",
#         "text": "A text message sent using the Nexmo SMS API",
#     }
# )

# if responseData["messages"][0]["status"] == "0":
#     print("Message sent successfully.")
# else:
#     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
def send_sms(phone_number, message):
    if not phone_number.startswith('+'):
        phone_number = '+20' + phone_number.lstrip('0')
    # client = vonage.Client(key="394a44ac", secret="8rq5vbvHRSqcShYv")
    client = vonage.Client(key="0606299a", secret="C3Ku7R8yGAn9uzRl")

    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Wallet",
            "to": phone_number,
            "text": message,
        }
    )
    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

# client = vonage.Client(key="394a44ac", secret="8rq5vbvHRSqcShYv")
# sms = vonage.Sms(client)

# responseData = sms.send_message(
#     {
#         "from": "Vonage APIs",
#         "to": "201153155231",
#         "text": "A text message sent using the Nexmo SMS API",
#     }
# )

# if responseData["messages"][0]["status"] == "0":
#     print("Message sent successfully.")
# else:
#     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")