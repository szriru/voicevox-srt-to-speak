from pydub import AudioSegment

def pysrttime_to_seconds(t):
  return (t.hours * 60 + t.minutes) * 60 + t.seconds + t.milliseconds / 1000
  
def get_audio_query_url(voicevox_url, text, speaker):
  return f"{voicevox_url}/audio_query?text={text}&speaker={speaker}"

def get_synthesis_url(voicevox_url, speaker):
  return f"{voicevox_url}/synthesis?speaker={speaker}&enable_interrogative_upspeak=true"

# combine audios including silence time.
def combine_audio(srt_name, srt_start_end_set, max_audio_length):
  # Init audio
  combined_audio = AudioSegment.silent(duration=max_audio_length*1000, frame_rate=24000)

  for index, item in srt_start_end_set.items():
    # using fade_in to suppress a noise when putting sounds together.
    audio = AudioSegment.from_file(f"./output/{srt_name}/individual/{index}.wav").fade_in(duration=100)
    (srt_start, srt_end) = item
    srt_start_sec = srt_start * 1000
    combined_audio = combined_audio.overlay(audio, position=srt_start_sec)

  combined_audio.export(f"./output/{srt_name}/combined_audio.wav", format="wav")
  print(f"done. file location is: ./output/{srt_name}/combined_audio.wav")