from windows.function_widgets import VideoDetectionWidget

class VideoAnalysisWidget(VideoDetectionWidget):
    def __init__(self, url:str):
        super().__init__(url)
        self.upload_widget.set_url(f'{url}/admin/video_analysis')
        self.upload_widget.resultSignal.connect(self.show_result)

    def show_result(self, result):
        result = result['result']  # bool
        print(result)