import cv2
import os

def slice_video(frame_interval=1, path=os.getcwd(), write_path='10.27', crop="None"):
    data_path = os.path.join(path, "..", "src", write_path)
    videos_path = os.path.join(data_path, "videos")
    pictures_path = os.path.join(data_path, "pictures")

    width, _ = 640, 480

    if not os.path.exists(pictures_path):
        os.makedirs(pictures_path)

    videos = os.listdir(videos_path)
    for vid in videos:
        curr_vid_path = os.path.join(videos_path, vid)
        video_name = vid[:-4]
        print(f"Curr vid: {video_name}")

        video = cv2.VideoCapture(curr_vid_path)

        frame_count = 0
        while True:
            ret, frame = video.read()

            if not ret:
                print(f'end of the video: {video_name}')
                break

            frame_count += 1

            if (frame_count % frame_interval == 0):
                filename = f'{video_name}_{frame_count//frame_interval}.jpg'
                file_path = os.path.join(pictures_path, filename)
                if frame is None:
                    print(f'frame is None')
                else:
                    _, original_width = frame.shape[:2]
                    cropped_frame = frame[128:]  # removes the top 128 pixels
                    if crop == "drum": cropped_frame = cropped_frame[:, :original_width - width, :]
                    if crop == "head": cropped_frame = cropped_frame[:, original_width - width:, :]

                    cv2.imwrite(file_path, cropped_frame)

        video.release()       