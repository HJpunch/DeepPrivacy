import sys
from PyQt6.QtWidgets import QApplication
from windows.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(ip='192.168.1.230', port=18400)
    window.show()

    app.exec()


r"""
TODO

1. 로그인위젯 - stacked widget에 추가, flask로 로그인 구현
   flask에 /login route 파서 인증 후 인증되면 current widget 이미지 탐지로 변경
   로그아웃하면 다시 current widget 로그인위젯으로 설정

2. 파일 업로드 전 서버 연결 상태 확인 
   파일 업로드 하면 / route에 get 보내서 response code 200이면 그 때 업로드 하기
   -> 해결

3. 영상 인식 결과에서 DB 내 이미지 보이는 방법
   각 비디오 내에서 앞에서 5개 이미지만 끊어서 static 내에 cp 후 get해오기?

4. 로고 짤리는 문제
   -> 해결. setminimum size 삭제

5. 이미지 탐지 None인 거 따로 결과 위젯 만들기
   -> 해결.

6. 기능 바꿀 시 이전 기능 결과 clear
   -> 해결. 좀 이상하긴 한데 암튼 됨

7. 서버쪽 문제로 result 못 받아올 시 오류 dialog 띄우기

8. requests에 csrf token pass
   -> 그냥 쓰지 말자..

9. result에서 urllib 쓴 부분 requests로 교체
   -> 해결.
"""