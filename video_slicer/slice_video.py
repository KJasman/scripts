import cv2
import os
import glob
from typing import List

video_files: List[str] = glob.glob('/Videos/*.mp4')
video_files += glob.glob('/Videos/*.MP4')
# .. add more video file extensions as needed

if(len(video_files) == 0):
    print("No compatible video files found")
    exit()

for video_file in video_files:
    # Open video file
    video: cv2.VideoCapture = cv2.VideoCapture(video_file)
    print("Opened file successfully")
    
    # Get the frame rate of the video
    fps: float = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second: {0}".format(round(fps)))
    
    # Calculate the frame number to capture every 2 seconds
    per_n_seconds = 2.0
    frame_interval = round(per_n_seconds * fps)

    # Set frame counter
    frame_counter = 0
    
    # Set image index for naming
    image_index = 1

    # Create a new directory for each video
    base_name = os.path.basename(video_file)
    parsed_ext = os.path.splitext(base_name)[0]
    new_dir_path = 'Videos/Stills/{}'.format(parsed_ext)
    os.makedirs(new_dir_path, exist_ok=True)

    while True:
        # Read next frame when possible
        ret, frame = video.read()
        if not ret:
            print("Done with video")
            print("-------------------------")
            break  

        # If frame is at the desired interval
        if frame_counter % frame_interval == 0:
            # resize to 640 x 480 
            resized_frame = cv2.resize(frame, (640, 480))
            cv2.imwrite('{}/frame_{}_{}.png'.format(new_dir_path, parsed_ext, image_index), resized_frame)
            
            image_index += 1

        # Increment frame counter
        frame_counter += 1
        
    
    # Close video file when the last frame is reached
    video.release()