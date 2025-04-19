---
machine-display: false
---

# Text-to-Speech

{% hint style="warning" %}

**BrainyFlow does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index.md#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

| **Service**          | **Free Tier**       | **Pricing Model**                                            | **Docs**                                                                                  |
| -------------------- | ------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Amazon Polly**     | 5M std + 1M neural  | ~$4 /M (std), ~$16 /M (neural) after free tier               | [Polly Docs](https://aws.amazon.com/polly/)                                               |
| **Google Cloud TTS** | 4M std + 1M WaveNet | ~$4 /M (std), ~$16 /M (WaveNet) pay-as-you-go                | [Cloud TTS Docs](https://cloud.google.com/text-to-speech)                                 |
| **Azure TTS**        | 500K neural ongoing | ~$15 /M (neural), discount at higher volumes                 | [Azure TTS Docs](https://azure.microsoft.com/products/cognitive-services/text-to-speech/) |
| **IBM Watson TTS**   | 10K chars Lite plan | ~$0.02 /1K (i.e. ~$20 /M). Enterprise options available      | [IBM Watson Docs](https://www.ibm.com/cloud/watson-text-to-speech)                        |
| **ElevenLabs**       | 10K chars monthly   | From ~$5/mo (30K chars) up to $330/mo (2M chars). Enterprise | [ElevenLabs Docs](https://elevenlabs.io)                                                  |

## Example Code

### 1. Amazon Polly

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install boto3
import boto3
import os

def synthesize_polly(text: str, output_filename: str = "polly_output.mp3", region: str | None = None):
    """Synthesizes speech using AWS Polly."""
    # Assumes AWS credentials are configured (e.g., via env vars, ~/.aws/credentials)
    aws_region = region or os.environ.get("AWS_REGION", "us-east-1")
    try:
        polly = boto3.client("polly", region_name=aws_region)
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna" # Example voice
        )

        # Check if AudioStream is present
        if "AudioStream" in response:
            with open(output_filename, "wb") as f:
                f.write(response["AudioStream"].read())
            print(f"Audio saved to {output_filename}")
        else:
            print("Error: Could not stream audio from Polly.")

    except Exception as e:
        print(f"Error calling AWS Polly: {e}")

# Example:
# synthesize_polly("Hello from AWS Polly!")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @aws-sdk/client-polly @aws-sdk/node-http-handler
import * as fs from 'fs'
import { Writable } from 'stream' // Import Writable
import { PollyClient, SynthesizeSpeechCommand } from '@aws-sdk/client-polly'
import { NodeHttpHandler } from '@aws-sdk/node-http-handler' // Required for streaming body

async function synthesizePolly(
  text: string,
  outputFilename: string = 'polly_output.mp3',
  region?: string,
): Promise<void> {
  /** Synthesizes speech using AWS Polly. */
  // Assumes AWS credentials are configured (e.g., via env vars, instance profile)
  const awsRegion = region || process.env.AWS_REGION || 'us-east-1'
  const client = new PollyClient({ region: awsRegion })

  const command = new SynthesizeSpeechCommand({
    Text: text,
    OutputFormat: 'mp3',
    VoiceId: 'Joanna', // Example voice
  })

  try {
    const response = await client.send(command)

    if (response.AudioStream) {
      // Handle the streaming body (Readable)
      const audioStream = response.AudioStream as NodeJS.ReadableStream // Cast for Node.js environment
      const fileStream = fs.createWriteStream(outputFilename)

      // Pipe the audio stream to the file
      await new Promise((resolve, reject) => {
        audioStream.pipe(fileStream)
        fileStream.on('finish', resolve)
        fileStream.on('error', reject)
        audioStream.on('error', reject) // Handle errors on the audio stream too
      })

      console.log(`Audio saved to ${outputFilename}`)
    } else {
      console.error('Error: Could not stream audio from Polly.')
    }
  } catch (error) {
    console.error('Error calling AWS Polly:', error)
  }
}

// Example:
// synthesizePolly("Hello from AWS Polly!");
```

{% endtab %}
{% endtabs %}

### 2. Google Cloud TTS

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install google-cloud-texttospeech
from google.cloud import texttospeech
import os

def synthesize_google_tts(text: str, output_filename: str = "gcloud_tts_output.mp3"):
    """Synthesizes speech using Google Cloud TTS."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
    try:
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        # Example voice, check documentation for more options
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        with open(output_filename, "wb") as f:
            f.write(response.audio_content)
        print(f"Audio saved to {output_filename}")

    except Exception as e:
        print(f"Error calling Google Cloud TTS: {e}")

# Example:
# synthesize_google_tts("Hello from Google Cloud Text-to-Speech!")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @google-cloud/text-to-speech
import * as fs from 'fs'
import { promisify } from 'util'
import textToSpeech from '@google-cloud/text-to-speech'

const writeFileAsync = promisify(fs.writeFile)

async function synthesizeGoogleTts(
  text: string,
  outputFilename: string = 'gcloud_tts_output.mp3',
): Promise<void> {
  /** Synthesizes speech using Google Cloud TTS. */
  // Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
  try {
    const client = new textToSpeech.TextToSpeechClient()
    const request = {
      input: { text: text },
      // Example voice, check documentation for more options
      voice: { languageCode: 'en-US', ssmlGender: 'NEUTRAL' as const }, // Use 'as const' for enum-like strings
      audioConfig: { audioEncoding: 'MP3' as const },
    }

    const [response] = await client.synthesizeSpeech(request)

    if (response.audioContent) {
      await writeFileAsync(outputFilename, response.audioContent, 'binary')
      console.log(`Audio saved to ${outputFilename}`)
    } else {
      console.error('Error: No audio content received from Google Cloud TTS.')
    }
  } catch (error) {
    console.error('Error calling Google Cloud TTS:', error)
  }
}

// Example:
// synthesizeGoogleTts("Hello from Google Cloud Text-to-Speech!");
```

{% endtab %}
{% endtabs %}

### 3. Azure TTS

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
import os

def synthesize_azure_tts(text: str, output_filename: str = "azure_tts_output.wav"):
    """Synthesizes speech using Azure Cognitive Services TTS."""
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        print("Error: AZURE_SPEECH_KEY or AZURE_SPEECH_REGION not set.")
        return

    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Example voice, check documentation for more
        # speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

        # Synthesize to an audio file
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Audio saved to {output_filename}")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")

    except Exception as e:
        print(f"Error calling Azure TTS: {e}")

# Example:
# synthesize_azure_tts("Hello from Azure Text-to-Speech!")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install microsoft-cognitiveservices-speech-sdk
import * as fs from 'fs' // Only needed if saving to file manually, SDK handles it
import * as sdk from 'microsoft-cognitiveservices-speech-sdk'

function synthesizeAzureTts(
  text: string,
  outputFilename: string = 'azure_tts_output.wav',
): Promise<void> {
  /** Synthesizes speech using Azure Cognitive Services TTS. */
  return new Promise((resolve, reject) => {
    const speechKey = process.env.AZURE_SPEECH_KEY
    const serviceRegion = process.env.AZURE_SPEECH_REGION

    if (!speechKey || !serviceRegion) {
      console.error('Error: AZURE_SPEECH_KEY or AZURE_SPEECH_REGION not set.')
      return reject(new Error('Azure credentials not set.'))
    }

    const speechConfig = sdk.SpeechConfig.fromSubscription(speechKey, serviceRegion)
    // Example voice, check documentation for more
    // speechConfig.speechSynthesisVoiceName = "en-US-JennyNeural";

    // Synthesize to an audio file directly using the SDK
    const audioConfig = sdk.AudioConfig.fromAudioFileOutput(outputFilename)

    const synthesizer = new sdk.SpeechSynthesizer(speechConfig, audioConfig)

    synthesizer.speakTextAsync(
      text,
      (result) => {
        if (result.reason === sdk.ResultReason.SynthesizingAudioCompleted) {
          console.log(`Audio saved to ${outputFilename}`)
          resolve()
        } else {
          console.error(`Speech synthesis canceled: ${result.errorDetails}`)
          reject(new Error(`Speech synthesis failed: ${result.errorDetails}`))
        }
        synthesizer.close() // Close synthesizer after completion/error
      },
      (error) => {
        console.error(`Error during synthesis: ${error}`)
        synthesizer.close()
        reject(error)
      },
    )
  })
}

// Example:
// synthesizeAzureTts("Hello from Azure Text-to-Speech!")
//     .then(() => console.log("Azure TTS synthesis finished."))
//     .catch(error => console.error("Azure TTS synthesis failed:", error));
```

{% endtab %}
{% endtabs %}

### 4. IBM Watson TTS

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install ibm_watson
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

def synthesize_ibm_tts(text: str, output_filename: str = "ibm_tts_output.mp3"):
    """Synthesizes speech using IBM Watson TTS."""
    api_key = os.environ.get("IBM_API_KEY")
    service_url = os.environ.get("IBM_SERVICE_URL")

    if not api_key or not service_url:
        print("Error: IBM_API_KEY or IBM_SERVICE_URL not set.")
        return

    try:
        authenticator = IAMAuthenticator(api_key)
        text_to_speech = TextToSpeechV1(authenticator=authenticator)
        text_to_speech.set_service_url(service_url)

        response = text_to_speech.synthesize(
            text=text,
            voice='en-US_AllisonV3Voice', # Example voice
            accept='audio/mp3' # Specify desired format
        ).get_result()

        # The result object has a 'content' attribute with the audio data
        with open(output_filename, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"Audio saved to {output_filename}")

    except Exception as e:
        print(f"Error calling IBM Watson TTS: {e}")

# Example:
# synthesize_ibm_tts("Hello from IBM Watson Text-to-Speech!")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install ibm-watson
import * as fs from 'fs'
import { promisify } from 'util'
import { IamAuthenticator } from 'ibm-watson/auth'
import TextToSpeechV1 from 'ibm-watson/text-to-speech/v1'

const writeFileAsync = promisify(fs.writeFile)

async function synthesizeIbmTts(
  text: string,
  outputFilename: string = 'ibm_tts_output.mp3',
): Promise<void> {
  /** Synthesizes speech using IBM Watson TTS. */
  const apiKey = process.env.IBM_API_KEY
  const serviceUrl = process.env.IBM_SERVICE_URL

  if (!apiKey || !serviceUrl) {
    console.error('Error: IBM_API_KEY or IBM_SERVICE_URL not set.')
    return
  }

  try {
    const textToSpeech = new TextToSpeechV1({
      authenticator: new IamAuthenticator({ apikey: apiKey }),
      serviceUrl: serviceUrl,
    })

    const synthesizeParams = {
      text: text,
      voice: 'en-US_AllisonV3Voice', // Example voice
      accept: 'audio/mp3', // Specify desired format
    }

    const response = await textToSpeech.synthesize(synthesizeParams)
    // The response body is a ReadableStream in Node.js
    const audioBuffer = await streamToBuffer(response.result as NodeJS.ReadableStream)

    await writeFileAsync(outputFilename, audioBuffer)
    console.log(`Audio saved to ${outputFilename}`)
  } catch (error) {
    console.error('Error calling IBM Watson TTS:', error)
  }
}

// Helper function to convert a ReadableStream to a Buffer
function streamToBuffer(stream: NodeJS.ReadableStream): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = []
    stream.on('data', (chunk) => chunks.push(chunk))
    stream.on('error', reject)
    stream.on('end', () => resolve(Buffer.concat(chunks)))
  })
}

// Example:
// synthesizeIbmTts("Hello from IBM Watson Text-to-Speech!");
```

{% endtab %}
{% endtabs %}

### 5. ElevenLabs

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install requests
import requests
import os

def synthesize_elevenlabs(text: str, output_filename: str = "elevenlabs_output.mp3"):
    """Synthesizes speech using ElevenLabs API."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    # Find voice IDs via ElevenLabs website or API
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Example: Rachel

    if not api_key:
        print("Error: ELEVENLABS_API_KEY not set.")
        return
    if not voice_id:
        print("Error: ELEVENLABS_VOICE_ID not set.")
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg", # Request MP3 format
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1", # Or other models like eleven_multilingual_v2
        "voice_settings": {
            "stability": 0.5,       # Example settings
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() # Raise exception for bad status codes

        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Audio saved to {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error calling ElevenLabs API: {e}")
        # Print response body if available for more details
        if e.response is not None:
             print(f"Response body: {e.response.text}")


# Example:
# synthesize_elevenlabs("Hello from ElevenLabs Text-to-Speech!")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Uses fetch API, no specific SDK needed unless desired
import * as fs from 'fs'
import { promisify } from 'util'

const writeFileAsync = promisify(fs.writeFile)

async function synthesizeElevenlabs(
  text: string,
  outputFilename: string = 'elevenlabs_output.mp3',
): Promise<void> {
  /** Synthesizes speech using ElevenLabs API. */
  const apiKey = process.env.ELEVENLABS_API_KEY
  // Find voice IDs via ElevenLabs website or API
  const voiceId = process.env.ELEVENLABS_VOICE_ID || '21m00Tcm4TlvDq8ikWAM' // Example: Rachel

  if (!apiKey) {
    console.error('Error: ELEVENLABS_API_KEY not set.')
    return
  }
  if (!voiceId) {
    console.error('Error: ELEVENLABS_VOICE_ID not set.')
    return
  }

  const url = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`
  const headers: HeadersInit = {
    Accept: 'audio/mpeg',
    'Content-Type': 'application/json',
    'xi-api-key': apiKey,
  }
  const body = JSON.stringify({
    text: text,
    model_id: 'eleven_monolingual_v1', // Or other models
    voice_settings: {
      stability: 0.5,
      similarity_boost: 0.75,
    },
  })

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: body,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, message: ${await response.text()}`)
    }

    // Get response body as ArrayBuffer
    const audioArrayBuffer = await response.arrayBuffer()
    // Convert ArrayBuffer to Buffer for writing to file
    const audioBuffer = Buffer.from(audioArrayBuffer)

    await writeFileAsync(outputFilename, audioBuffer)
    console.log(`Audio saved to ${outputFilename}`)
  } catch (error) {
    console.error('Error calling ElevenLabs API:', error)
  }
}

// Example:
// synthesizeElevenlabs("Hello from ElevenLabs Text-to-Speech!");
```

{% endtab %}
{% endtabs %}
