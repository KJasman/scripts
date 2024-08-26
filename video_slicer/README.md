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
- Creates separate folders for each video's frames
- Uses multithreading for concurrent video processing
- Provides simple console output for tracking progress
- Optimized for efficient frame extraction, especially for large videos

## How it works

1. The script searches for all video files (currently .mp4 and .MP4) in the specified directory and its subdirectories.
2. It creates a 'Stills' directory at the same level as the input directory to store extracted frames.
3. For each video file found, the script:
   - Opens the video file
   - Calculates the frame interval to extract a frame every 5 seconds
   - Creates a subdirectory for the video's frames within the 'Stills' directory, named after the video file
   - Extracts frames at the calculated interval, resizing them to 640x480
   - Saves the frames as JPEG images in the corresponding subdirectory
4. The script processes multiple videos concurrently using multithreading.

## Usage

Run the script from the command line, providing the absolute path to the directory containing your videos:

```
python video_frame_extractor.py /path/to/your/video/directory
```

## Output

The extracted frames will be saved in a 'Stills' directory created at the same level as the input directory. Each video will have its own subdirectory within the 'Stills' directory, named after the original video file.

Each frame is saved as a JPEG file named '{video_name}_frame_{index}.jpeg' within its corresponding video subdirectory.

### Resulting Directory Structure:

```
Stills/
├── video1_name/
│   ├── video1_name_frame_1.jpeg
│   ├── video1_name_frame_2.jpeg
│   └── ...
├── video2_name/
│   ├── video2_name_frame_1.jpeg
│   ├── video2_name_frame_2.jpeg
│   └── ...
└── ...
```

The script provides console output indicating:
- The number of video files found
- Which video is currently being processed
- A completion message for each video, including the number of frames extracted
- A final message when all videos have been processed

## Notes

- The script currently supports .mp4 and .MP4 video files. You can modify the script to include additional video formats if needed.
- Frames are extracted every 5 seconds. You can adjust this interval by modifying the `frame_interval` calculation in the `process_video` function.
- The script uses multithreading to process videos concurrently, with the number of threads equal to the system's logical CPU count.
- The frame extraction process has been optimized to efficiently handle large videos by directly seeking to the desired frames instead of reading through all frames sequentially.

## Optimization

The script has been optimized for efficient frame extraction:
- It uses `video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)` to directly seek to the desired frames, reducing unnecessary frame reads.
- The main processing loop has been simplified, potentially improving performance for large numbers of frames.
- Memory usage is kept efficient by processing one frame at a time instead of loading all frames into memory.

## Customization

You can further customize the script by:
- Modifying the `frame_interval` calculation to change the frequency of extracted frames.
- Adjusting the resizing dimensions in the `cv2.resize()` function call.
- Adding support for additional video formats by modifying the file extension check in the `find_video_files` function.
