Below is a **minimal** version that:

1. Prompts for a topic  
2. Searches YouTube  
3. Prints results  
4. (Optionally) sends them via email  

Feel free to **uncomment** or add code to summarize results with an LLM if desired.

```python
import os
import googleapiclient.discovery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# If you want to summarize with an LLM, uncomment these:
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

def search_youtube(query, max_results=5):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY not set. Please set it in your environment.")
        return []

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            video_title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            videos.append({"title": video_title, "id": video_id})
    return videos

def send_email(sender, password, recipient, subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Optional LLM summarization function
# def summarize_videos(video_list):
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     llm = OpenAI(openai_api_key=openai_api_key)
#
#     prompt = PromptTemplate(
#         input_variables=["videos"],
#         template="Here are some video titles:\n{videos}\nPlease provide a concise summary."
#     )
#
#     chain = LLMChain(llm=llm, prompt=prompt)
#     videos_text = "\n".join([f"- {v['title']}" for v in video_list])
#     summary = chain.run(videos=videos_text)
#     return summary

def main():
    topic = input("Enter a topic to search on YouTube: ")
    videos = search_youtube(topic)

    if not videos:
        print("No videos found or missing API key.")
        return

    print(f"\nFound {len(videos)} videos on '{topic}':")
    for v in videos:
        print(f"- {v['title']} (https://youtube.com/watch?v={v['id']})")

    # (Optional) Summarize results with an LLM
    # summary = summarize_videos(videos)
    # print("\nSummary of these videos:\n", summary)

    choice = input("\nDo you want to send these results via email? (y/n) ")
    if choice.lower() == 'y':
        sender_email = input("Your email (sender): ")
        sender_pass = input("Your email password (or app password): ")
        recipient_email = input("Recipient email: ")

        # Prepare email body (simple version)
        body = "Here are the videos we found:\n"
        for v in videos:
            body += f"- {v['title']}: https://youtube.com/watch?v={v['id']}\n"

        # If you had a summary, you could add it here:
        # body += f"\nSummary:\n{summary}"

        send_email(
            sender=sender_email,
            password=sender_pass,
            recipient=recipient_email,
            subject=f"YouTube Search Results for {topic}",
            body=body
        )

if __name__ == "__main__":
    main()

