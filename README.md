SRTファイルを読み込み,各セリフ時間内に収まるように考慮してVoicevox Engine APIを利用して音声合成をします。

## 使い方

1. ``` git clone https://github.com/szriru/voicevox-srt-to-speak ```
2. ``` cd voicevox-srt-to-speak ```
3. ``` pip install -r requirement.txt ```
4. ``` python main.py "input.srt" ```
"input.srt"を実際のsrtファイルの名前・場所にしてください


## オプション

``` --speaker ``` スピーカーID,デフォルトは3のノーマルずんだもん.

``` --voicevox_url ``` voicevox engineがapiをexposeしているURL.デフォルトはhttp://127.0.0.1:50021

## このレポジトリを使った例

[![Watch the video](https://img.youtube.com/vi/SalqafD0ckQ/default.jpg)](https://youtu.be/SalqafD0ckQ)

[![Watch the video](https://img.youtube.com/vi/t9sJQkFUAF8/default.jpg)](https://youtu.be/t9sJQkFUAF8)

## 追加する機能

- キャラを分けられるようにする。
- 


## License

MIT