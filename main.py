

# import gradio as gr
# import base64
# import requests
# import json
# import io
# import time

# # 🔑 Giev API Key (replace with your valid key)
# API_KEY = "YOUR_GIEV_API_KEY"
# GIEV_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# # 🔍 Function to classify image with Giev
# def classify_with_giev(image):
#     # Convert image to base64
#     buffered = image.convert("RGB")
#     buf = io.BytesIO()
#     buffered.save(buf, format="JPEG")
#     img_bytes = buf.getvalue()
#     img_b64 = base64.b64encode(img_bytes).decode("utf-8")

#     # Giev prompt
#     prompt = (
#         "Look at this item and classify it clearly as either "
#         "'♻ Recyclable' or '🚫 Non-Recyclable'. "
#         "Then explain briefly why."
#     )

#     # Payload with image + text
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": prompt},
#                     {
#                         "inline_data": {
#                             "mime_type": "image/jpeg",
#                             "data": img_b64
#                         }
#                     }
#                 ]
#             }
#         ]
#     }

#     headers = {"Content-Type": "application/json"}

#     # Send request
#     response = requests.post(GIEV_URL, headers=headers, data=json.dumps(payload))

#     if response.status_code == 200:
#         data = response.json()
#         try:
#             explanation = data["candidates"][0]["content"]["parts"][0]["text"]
#         except (KeyError, IndexError):
#             explanation = "Giev classifier did not return a valid response."
#     else:
#         explanation = f"API error: {response.status_code} - {response.text}"

#     # 🔎 Extract status (Recyclable / Non-Recyclable)
#     if "Recyclable" in explanation:
#         status = "♻ Recyclable"
#         color = "green"
#     else:
#         status = "🚫 Non-Recyclable"
#         color = "red"

#     # 🔄 Animated typing effect for explanation
#     animated_html = f"""
#     <div style="font-size:22px; font-weight:bold; color:{color}; animation: blink 1s infinite;">
#         {status}
#     </div>
#     <div style="margin-top:10px; font-size:16px; font-family:monospace; white-space:pre-wrap;">
#     """

#     for i in range(1, len(explanation) + 1):
#         yield animated_html + explanation[:i] + "</div>"
#         time.sleep(0.02)  # typing speed

#     # Add CSS animation
#     yield animated_html + explanation + """
#     <style>
#     @keyframes blink {
#         50% { opacity: 0.3; }
#     }
#     </style>
#     </div>
#     """

# # 🎨 Gradio UI
# demo = gr.Interface(
#     fn=classify_with_giev,
#     inputs=gr.Image(type="pil", label="Upload Giev Image"),
#     outputs=gr.HTML(label="Giev Classification & Explanation"),
#     title="♻ Giev Classifier",
#     description="Upload an image and Giev will classify it as recyclable or non-recyclable with an animated explanation."
# )

# # 🚀 Launch with share link
# demo.launch(share=True)
