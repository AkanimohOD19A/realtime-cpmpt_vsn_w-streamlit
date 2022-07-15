import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

st.title("Realtime Detection")
st.write("First Trail")


## Developing the Stream Component
### Fundamental
class VideoProcessor:
    def __init__(self) -> None:
        self.threshold1 = 100
        self.threshold2 = 200

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        ## Canny edge detection filter and GrayScale converter
        img = cv2.cvtColor(cv2.Canny(img,
                                     self.threshold1,
                                     self.threshold2), cv2.COLOR_GRAY2BGR)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(key="example",
                      video_processor_factory=VideoProcessor,
                      rtc_configuration={
                          "iceservers": [{"urls": ["stun:stun.1.google.com:19302"]}]
                      }
                      )
## i.e if the instance of video processing is active then..
if ctx.video_processor:
    ctx.video_processor.threshold1 = st.slider("Threshold1",
                                               min_value=0, max_value=1000,
                                               step=1, value=100)
    ctx.video_processor.threshold2 = st.slider("Threshold1",
                                               min_value=0, max_value=1000,
                                               step=1, value=200)


### NOTICE {ABT recv()}
##1. The global keyword does not work as expected inside .recv().
##2. Streamlit methods such as st.write() cannot be used inside .recv().
##3. Communications between inside and outside .recv() must be thread-safe.

# +=> DEPLOYMENT
# To deploy the app to the cloud, we have to add rtc_configuration
# parameter to the webrtc_streamer().
## The value of the rtc_configuration argument will be
# passed to the RTCPeerConnection constructor on the frontend.