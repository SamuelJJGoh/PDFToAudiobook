from pypdf import PdfReader
import boto3

reader = PdfReader("sample.pdf")
page = reader.pages[0]
text  = page.extract_text()

polly = boto3.client("polly", region_name="eu-west-2")  # pick your region

response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",       
    VoiceId="Amy",            # e.g., en-GB: Amy, Emma, Brian
    Engine="neural"           
)

with open("test.mp3", "wb") as f:
    f.write(response["AudioStream"].read())
