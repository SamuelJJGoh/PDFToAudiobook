from pypdf import PdfReader
import boto3, html

pdf = "RainStory.pdf"
reader = PdfReader(pdf)

if reader.is_encrypted and reader.decrypt("") == 0:
    raise ValueError("PDF is encrypted and needs a password.")

def norm(text: str) -> str:
    return html.escape((text or "").strip())

pages = reader.pages[3:25]

parts = []
for idx, p in enumerate(pages, start=1):
    page_text = norm(p.extract_text())
    if not page_text:
        continue
    parts.append(f"<p>{page_text}</p>")
    if idx != len(pages):  # no pause after the last page
        parts.append("<break time='0.5s'/>")

ssml = f"<speak>{''.join(parts)}</speak>"

polly = boto3.client("polly", region_name="eu-west-2") 

response = polly.synthesize_speech(
    Text=ssml,
    TextType="ssml",
    OutputFormat="mp3",       
    VoiceId="Amy",            # e.g., en-GB: Amy, Emma, Brian
    Engine="neural"           
)

with open("rainstory.mp3", "wb") as f:
    f.write(response["AudioStream"].read())
