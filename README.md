# En Passant - Chess Commentary for Pear VC + OpenAI Hackathon

## How to Run

### Step 1
Run `bash setup.sh` to setup the python venv

### Step 2
Navigate to ElevenLabs -> Voices -> Click on "Add Generative or Cloned Voice" -> Click on "Instant Voice Cloning" and create a voice for Aziz using the audio file of Aziz from audio/ folder. Select the audio file for Gordon depending on the tone you prefer.

### Step 3
Repeat the same process as Step 2 but for Gordon. Navigate to ElevenLabs -> Voices -> Click on "Add Generative or Cloned Voice" -> Click on "Instant Voice Cloning" and create a voice for Gordon using one of the two audio files of Gordon from audio/ folder. Select the audio file for Gordon depending on the tone you prefer.

### Step 4
For each of the two voices, hover over the top right icon labeled "ID" to find the Voice ID for each voice.

### Step 5
Fill in the following fields in the .env file:

* `OPENAI_API_KEY` - OpenAI Key
* `ELEVEN_LABS_API` - Eleven Labs API Key
* `GORDON_VOICE_ID` - Voice ID for Gordon from ElevenLabs that you found on Step 4
* `AZIZ_VOICE_ID` - Voice ID for Aziz from ElevenLabs that you found on Step 4


### Step 6
Run the following command to run the application locally:

`streamlit run main_page.py`


## Hackathon Results

Results can be seen in this link: https://pear.vc/events/pear-vc-x-open-ai-hackathon/

We won "Most Innovative Application" Award at Pear VC + OpenAI Hackathon. See  below.

![Hackathon Awards](./PearVC_OpenAI_Hackathon_Awards.png "Hackathon Awards")

![Hackathon Projects](./PearVC_OpenAI_Hackathon_Projects.png "Hackathon Projects")

## Youtube Demo
* https://www.youtube.com/watch?v=VkvmBz_oC80
