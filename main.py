from pypdf import PdfReader
import boto3, html, re

PDF = "LittleHedgehogStory.pdf" # change PDF 
reader = PdfReader(PDF)
PAGES = reader.pages[2:9] # change which pages user wants


if reader.is_encrypted and reader.decrypt("") == 0:
    raise ValueError("PDF is encrypted and needs a password.")

def clean_for_ssml(s: str) -> str:
    if not s:
        return ""
    # de-hyphenate line wraps like "environ-\nment" -> "environment"
    s = re.sub(r"(\w)-\n(\w)", r"\1\2", s)
    # single newlines (line wraps) -> space; preserve paragraph breaks (\n\n)
    s = re.sub(r"(?<!\n)\n(?!\n)", " ", s)
    # collapse multiple spaces
    s = re.sub(r"[ \t\f\v]+", " ", s)
    # remove any remaining isolated artifact tokens
    s = re.sub(r"\btext(?:e)?\b", "", s, flags=re.IGNORECASE)
    return html.escape(s.strip())

parts = []
for idx, p in enumerate(PAGES, start=1):
    raw = p.extract_text()  
    page_text = clean_for_ssml(raw)
    if not page_text:
        continue
    parts.append(f"<p>{page_text}</p>")
    if idx != len(PAGES):  # no pause after the last page
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

with open("hedgehog.mp3", "wb") as f:
    f.write(response["AudioStream"].read())
