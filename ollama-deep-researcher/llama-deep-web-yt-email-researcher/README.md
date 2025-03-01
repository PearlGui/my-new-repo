# llama-deep-web-yt-email-researcher/main.py
import os
import googleapiclient.discovery

def search_youtube(query, max_results=5):
    api_key = os.getenv("YOUTUBE_API_KEY")  # or however you store it
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
    
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def summarize_videos(video_list):
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    prompt = PromptTemplate(
        input_variables=["video_info"],
        template="You are an AI that summarizes video titles. Here is the list:\n{video_info}\nProvide a short summary."
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    # Convert video list to text
    videos_text = "\n".join([f"{v['title']} (ID: {v['id']})" for v in video_list])
    summary = chain.run(video_info=videos_text)
    return summary
