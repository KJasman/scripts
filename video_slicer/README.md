# Video Frame Extractor

This Python script extracts frames from video files in a specified directory and its subdirectories. It uses the OpenCV library to process videos and save frames as images.

## Dependencies

- OpenCV (cv2)
- os
- typing
- argparse
- concurrent.futures
- multiprocessing

## Features

- Recursively searches for video files in the specified directory and its subdirectories
- Extracts frames at 5-second intervals from each video
- Resizes frames to 640x480 resolution
- Saves frames as JPEG images
- Maintains directory structure for extracted frames
- Uses multithreading for concurrent video processing
- Provides simple console output for tracking progress

## How it works

1. The script searches for all video files (currently .mp4 and .MP4) in the specified directory and its subdirectories.
2. It creates a 'Stills' directory at the same level as the input directory to store extracted frames.
3. For each video file found, the script:
   - Opens the video file
   - Calculates the frame interval to extract a frame every 5 seconds
   - Creates a subdirectory for the video's frames, maintaining the original directory structure
   - Extracts frames at the calculated interval, resizing them to 640x480
   - Saves the frames as JPEG images in the corresponding subdirectory
4. The script processes multiple videos concurrently using multithreading.

## Usage

Run the script from the command line, providing the absolute path to the directory containing your videos: `python video_frame_extractor.py /path/to/your/video/directory`

## Output

The extracted frames will be saved in a 'Stills' directory created at the same level as the input directory. The original directory structure is maintained within the 'Stills' directory.

Each frame is saved as a JPEG file named 'frame_{index}.jpeg' within a subdirectory corresponding to its source video.

The script provides console output indicating:
- The number of video files found
- Which video is currently being processed
- A completion message for each video, including the number of frames extracted
- A final message when all videos have been processed

## Notes

- The script currently supports .mp4 and .MP4 video files. You can modify the script to include additional video formats if needed.
- Frames are extracted every 5 seconds. You can adjust this interval by modifying the `frame_interval` calculation in the `process_video` function.
- The script uses multithreading to process videos concurrently, with the number of threads equal to the system's logical CPU count.