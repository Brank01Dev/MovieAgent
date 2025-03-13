import tkinter as tk
from tkinter import scrolledtext
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from googleapiclient.discovery import build


GOOGLE_API_KEY = "Please enter your Google API key"
GOOGLE_CSE_ID = "Please enter your Google CSE ID"
YOUTUBE_API_KEY = "Please enter your YouTube API key"
OPENAI_API_KEY = "Please enter your OpenAI API key"


chatbot = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

def google_search(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=query, cx=GOOGLE_CSE_ID).execute()
    if "items" in res:
        return res["items"][:1]  
    else:
        return []

def youtube_search_v3(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query + " official trailer",
        part="snippet",
        maxResults=1,
        type="video"
    )
    response = request.execute()

    if response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return "Error fetching YouTube video, please try again later."

def chat_with_ai():
    user_input = entry.get()
    if not user_input:
        log.insert(tk.END, "Enter questions for movies!\n")
        return

    entry.delete(0, tk.END)
    
    log.insert(tk.END, f"User: {user_input}\n")
    log.see(tk.END)

    try:
        messages = [
            SystemMessage(content="You are a helpful AI agent specializing in movies. Provide detailed information about movies, directors, actors, and give recommendations."),
            HumanMessage(content=user_input)
        ]
        ai_response = chatbot(messages).content

        if "movie" in user_input.lower():
            search_results = google_search(user_input + " IMDb")
            search_text = "\nIMDb Search Results:\n"
            for item in search_results:
                search_text += f"{item['title']}: {item['link']}\n"

            youtube_link = youtube_search_v3(user_input)
            search_text += f"\nYouTube Official Trailer: {youtube_link}\n"
            ai_response += f"\n\n{search_text}"

        log.insert(tk.END, f"AI: {ai_response}\n\n")
        log.see(tk.END)
    except Exception as e:
        log.insert(tk.END, f"Error: something went wrong, please try again\n")
        log.see(tk.END)

root = tk.Tk()
root.title("MOVIE SEARCH ENGINE")
root.geometry("700x400")
root.resizable(False, False)
root.configure(bg='gray')  

frame = tk.Frame(root, bg='white') 
frame.pack(pady=10)

entry = tk.Entry(frame, width=60, bg='white', fg='black')  
entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(frame, text="Ask agent", command=chat_with_ai, bg='white', fg='black')  
search_btn.pack(side=tk.LEFT)

log = scrolledtext.ScrolledText(root, width=80, height=20, bg='white', fg='black') 
log.pack(pady=10)
root.mainloop()