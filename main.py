import requests
import wave
import array
import io
import os
import pysrt
import argparse
from util import (
  pysrttime_to_seconds,
  get_audio_query_url,
  get_synthesis_url,
  combine_audio
)

def main():
  parser = argparse.ArgumentParser(description="TTS from SRT file in exact time through Voicevox Engine API")
  parser.add_argument("srt_file", help="srt file to convert")
  parser.add_argument("--speaker", help="speaker id. default is 3 (normal zundamon)", default=3)
  parser.add_argument("--voicevox_url", help="voicevox url that exposes its api", default="http://127.0.0.1:50021")
  args = parser.parse_args()
  
  speaker=args.speaker
  voicevox_url=args.voicevox_url
  srt_data = pysrt.open(args.srt_file)
  srt_name, _ = os.path.splitext(os.path.basename(args.srt_file))
  
  # { index: (start time, end time) }
  srt_start_end_set = {}
  
  # get max audio length from srt
  max_audio_length = pysrttime_to_seconds(srt_data[-1].end)
  
  if not srt_data or len(srt_data) == 0:
    raise ValueError("srt_data is empty")
  
  # generate individual audio.
  print("start generating individual audios.")
  for srt_index, srt_item in enumerate(srt_data):
    # prepare for an audio query
    text = srt_item.text
    start = pysrttime_to_seconds(srt_item.start)
    end = pysrttime_to_seconds(srt_item.end)
    srt_start_end_set[srt_index] = (start, end)
    srt_duration = pysrttime_to_seconds(srt_item.duration)
    audio_query_url = get_audio_query_url(voicevox_url, text, speaker)
    headers = {"accept": "application/json"}

    # audio query to voicevox api
    audio_query = requests.post(audio_query_url, headers=headers)
    audio_query_payload = audio_query.json()
  
    # calcurate length as normal speed
    # sum up all through consonant and vowel length including pause_mora
    sentence_length = 0
    for key, value in audio_query_payload.items():
      if key == "accent_phrases":
        for item in value:
          for key, value in item.items():
            if key == 'moras':
              for mora in value:
                if mora['consonant'] != None and mora['consonant_length'] != None:
                    sentence_length += mora['consonant_length']
                if mora['vowel'] != None and mora['vowel_length'] != None:
                    sentence_length += mora['vowel_length']
            elif key == 'pause_mora':
              if value is not None:
                if not value['consonant_length'] is None:
                  sentence_length += value['consonant_length']
                if not value['vowel_length'] is None:
                  sentence_length += value['vowel_length']

    # prepare for voice sythesis
    speedScale = 1.000
    # if an audio is expected to be longer than srt time, use speedScale.
    if sentence_length > srt_duration:
      speedScale = sentence_length / srt_duration
    synthesis_url = get_synthesis_url(voicevox_url, speaker)
    audio_query_payload['speedScale'] = speedScale
    headers = {
        "accept": "audio/wav",
        "Content-Type": "application/json"
    }
    r = requests.post(synthesis_url, json=audio_query_payload, headers=headers)
    
    if not os.path.exists(f"./output/{srt_name}/individual/"):
      os.makedirs(f"./output/{srt_name}/individual/")

    # Create a wave file with 32-bit sample width
    output_file = f"./output/{srt_name}/individual/{srt_index}.wav"
    with open(output_file, "wb") as f:
        audio_data = io.BytesIO(r.content)
        wave_writer = wave.open(f, 'wb')
        wave_writer.setnchannels(1)  # モノラル音声
        wave_writer.setsampwidth(2)  # 32ビットの場合は4バイト
        wave_writer.setframerate(24000)  # サンプリングレート
        wave_writer.writeframes(audio_data.getbuffer())
        wave_writer.close()
    
    print(f"{start}--{end}: {text}: done")
    
  
  combine_audio(srt_name, srt_start_end_set, max_audio_length)

if __name__ == '__main__':
  main()