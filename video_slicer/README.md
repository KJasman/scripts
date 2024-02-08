# Video Frame Extractor

This Python script is used to extract frames from video files. It uses the OpenCV library to read video files and write frames as images.

## Dependencies

- OpenCV (cv2)
- os
- glob

## How it works

The script first searches for all video files in the 'Videos' directory with the extensions '.mp4' and '.MP4'. You can add more video file extensions as needed.

If no compatible video files are found, the script will print a message and exit.

For each video file found, the script will:

1. Open the video file.
2. Get the frame rate of the video.
3. Calculate the frame number to capture every 2 seconds.
4. Read each frame in the video.
5. If the current frame is at the desired interval, it will save the frame as an image in the 'Stills' directory with the format 'frame_{video_name}_{frame_index}.png'.
6. Once all frames have been read, it will close the video file and move on to the next one.

## Usage

To use this script, simply run it in a Python environment where OpenCV is installed. Make sure your video files are in the 'Videos' directory.

\`\`\`python
python3 video_frame_extractor.py
\`\`\`

## Output

The output images will be saved in the 'Stills' directory. Each image will be named in the format 'frame_{video_name}_{frame_index}.png', where {video_name} is the name of the video file (without extension) and {frame_index} is the index of the frame in the video.

## Note

This script assumes that the 'Videos' and 'Stills' directories exist in the same directory as the script. If they do not exist, you will need to create them before running the script.