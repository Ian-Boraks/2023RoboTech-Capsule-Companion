import cv2

def play_video():
    video = cv2.VideoCapture('assets/wave.mp4')

    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

    while True:
        screen_width, screen_height = 3024, 1964
        ret, frame = video.read()
        if frame is not None:
            frame_height, frame_width, _ = frame.shape
            scaleWidth = float(screen_width)/float(frame_width)
            scaleHeight = float(screen_height)/float(frame_height)

            if scaleHeight>scaleWidth:
                imgScale = scaleWidth
            else:
                imgScale = scaleHeight

            newX,newY = frame.shape[1]*imgScale, frame.shape[0]*imgScale
            frame = cv2.resize(frame,(int(newX),int(newY)))

        if ret:
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            video = cv2.VideoCapture('assets/idle.mp4')
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            

    video.release()
    cv2.destroyAllWindows()
