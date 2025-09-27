from pypdf import PdfReader
import boto3

pdf = "RainStory.pdf"
reader = PdfReader(pdf)

if reader.is_encrypted:
    if reader.decrypt("") == 0:
        raise ValueError("PDF is encrypted and needs a password.")
    
num_of_pages = len(reader.pages)
pages = reader.pages

text = ""
for p in pages[3:25]:
    text += "".join(p.extract_text())

polly = boto3.client("polly", region_name="eu-west-2")  # pick your region

response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",       
    VoiceId="Amy",            # e.g., en-GB: Amy, Emma, Brian
    Engine="neural"           
)

with open("rainstory.mp3", "wb") as f:
    f.write(response["AudioStream"].read())
