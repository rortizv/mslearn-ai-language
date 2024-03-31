from dotenv import load_dotenv
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('es')  # Set target language to Spanish
        print('Ready to translate from ',translation_config.speech_recognition_language)

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)

        # Start translation
        Translate()

    except Exception as ex:
        print(ex)

def Translate():
    translation = ''

    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Speak now...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations['es']  # Translate to Spanish
    print(translation)

    # Synthesize translation
    speech_config.speech_synthesis_voice_name = "es-ES-ElviraNeural"  # Set Spanish voice
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


if __name__ == "__main__":
    main()