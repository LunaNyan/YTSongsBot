# YTSongsBot

## 요구 사항
- x86 또는 amd64 아키텍쳐의 컴퓨터
- Windows 7+ 또는 Linux
- Python 3.7+
- 적절한 오디오 출력 장치

## 설치 방법 (Windows)
1. [Python 3를 다운로드](https://www.python.org/downloads/)합니다. Python 3.7 또는 그 이상을 권장합니다. **설치 버튼을 누르기 전에 PATH 옵션을 체크하세요.**
2. [FFmpeg를 다운로드](https://ffmpeg.zeranoe.com/builds/)합니다.
3. FFmpeg 압축 파일을 열고 bin 안의 모든 파일을 C:\Windows\system32에 복사합니다.
4. YTSongs 레포지토리를 적절한 경로에 다운로드합니다.
5. cmd를 불러 `pip3 install -r requirements.txt`를 입력합니다.

실행 : sPlayer.py

## 설치 방법 (Linux)
```
git clone https://github.com/LunaNyan/YTSongsBot
cd YTSongsBot
sudo pip3 install -r requirements.txt
sudo apt install youtube-dl ffmpeg
```

실행 : `python3 sPlayer.py`

## 명령어
h - 도움말을 표시합니다.

r (검색어) - 곡을 검색한 뒤 플레이리스트에 추가합니다.

l - 플레이리스트를 출력합니다.

sf - 플레이리스트를 셔플합니다.

sk - 재생중인 곡을 스킵합니다.

del (숫자) - 지정된 플레이리스트 곡을 삭제합니다.

pr (숫자) - 지정된 플레이리스트 곡을 최상위로 올립니다.
