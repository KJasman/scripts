# Video Frame Extractor

This Python script extracts frames from video files in a specified directory and its subdirectories. It uses the OpenCV library to process videos and save frames as images.

## Dependencies

- OpenCV (cv2)
- os
- typing
- argparse
- tqdm

## Features

- Recursively searches for video files in the specified directory and its subdirectories
- Extracts frames at 2-second intervals from each video
- Resizes frames to 640x480 resolution (customizable)
- Saves frames as JPEG images
- Maintains directory structure for extracted frames
- Provides progress bars for overall processing and individual video frame extraction

## How it works

1. The script searches for all video files (currently .mp4 and .MP4) in the specified directory and its subdirectories.
2. It creates a 'Stills' directory at the same level as the input directory to store extracted frames.
3. For each video file found, the script:
   - Opens the video file
   - Calculates the frame interval to extract a frame every 2 seconds
   - Creates a subdirectory for the video's frames, maintaining the original directory structure
   - Extracts frames at the calculated interval, resizing them to 640x480
   - Saves the frames as JPEG images in the corresponding subdirectory

## Usage

Run the script from the command line, providing the absolute path to the directory containing your videos:

```
python video_frame_extractor.py /path/to/your/video/directory
```

## Output

The extracted frames will be saved in a 'Stills' directory created at the same level as the input directory. The original directory structure is maintained within the 'Stills' directory.

Each frame is saved as a JPEG file named 'frame_{index}.jpeg' within a subdirectory corresponding to its source video.

## Notes

- The script currently supports .mp4 and .MP4 video files. You can modify the script to include additional video formats if needed.
- Frames are extracted every 2 seconds. You can adjust this interval by modifying the `frame_interval` calculation in the `extract_frames` function.
- The script provides progress information and statistics for each video processed.