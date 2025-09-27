import boto3

polly = boto3.client("polly", region_name="eu-west-2")  # pick your region
text = "This is a short demo of the Amazon Polly written in Python"

response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",       
    VoiceId="Amy",            # e.g., en-GB: Amy, Emma, Brian
    Engine="neural"           
)

with open("test.mp3", "wb") as f:
    f.write(response["AudioStream"].read())
