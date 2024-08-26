import cv2  # OpenCV library for video processing
import os  # For file and directory operations
from typing import List  # For type hinting
import argparse  # For parsing command-line arguments
from tqdm import tqdm  # For progress bars


"""
Recursively find all video files in the given directory and its subdirectories.

Args:
base_path (str): The base directory to start the search.

Returns:
List[str]: A list of paths to video files.
"""
def find_video_files(base_path: str) -> List[str]:
    
    print(f"Searching for video files in {base_path}...")
    video_files = []
    # Walk through all directories and files in the base_path
    for root, _, files in os.walk(base_path):
        for file in files:
            # Check if the file has a video extension (currently .mp4 or .MP4)
            if file.lower().endswith(('.mp4', '.MP4')):  # Add more extensions if needed
                # Add the full path of the video file to our list
                video_files.append(os.path.join(root, file))
    print(f"Found {len(video_files)} video files.")
    return video_files


"""
Extract frames from all video files in the specified directory and its subdirectories.

Args:
base_path (str): The absolute path to the directory containing video files.
"""
def extract_frames(base_path: str):
    # Find all video files in the given directory and its subdirectories
    video_files = find_video_files(base_path)

    # If no video files are found, inform the user and exit the function
    if not video_files:
        print("No compatible video files found")
        return

    # Create a 'Stills' directory at the same level as the base path
    stills_base_path = os.path.join(os.path.dirname(base_path), 'Stills')
    os.makedirs(stills_base_path, exist_ok=True)
    print(f"Created 'Stills' directory at {stills_base_path}")

    # Process each video file
    for video_file in tqdm(video_files, desc="Processing videos", unit="video"):
        # Open the video file
        video = cv2.VideoCapture(video_file)
        print(f"\nProcessing: {video_file}")
        
        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        print(f"  Video info: {total_frames} frames, {fps:.2f} FPS, duration: {duration:.2f} seconds")
        
        # Calculate frame interval (extract a frame every 2 seconds)
        frame_interval = round(2.0 * fps)
        frame_counter = 0
        image_index = 1
        
        # Create a subdirectory for this video's frames
        relative_path = os.path.relpath(video_file, base_path)
        video_stills_path = os.path.join(stills_base_path, os.path.dirname(relative_path), os.path.splitext(os.path.basename(video_file))[0])
        os.makedirs(video_stills_path, exist_ok=True)
        print(f"  Saving frames to: {video_stills_path}")
        
        # Process frames with a progress bar
        with tqdm(total=total_frames, desc="  Extracting frames", unit="frame", leave=False) as pbar:
            while True:
                # Read the next frame
                ret, frame = video.read()
                if not ret:
                    break  # End of video
                
                # If we've reached a frame we want to extract
                if frame_counter % frame_interval == 0:
                    # Resize the frame to 640x480
                    resized_frame = cv2.resize(frame, (640, 480))
                    # Save the frame as a JPEG file
                    cv2.imwrite(os.path.join(video_stills_path, f'frame_{image_index}.jpeg'), resized_frame)
                    image_index += 1
                
                frame_counter += 1
                pbar.update(1)  # Update the progress bar
        
        # Close the video file
        video.release()
        print(f"  Extracted {image_index-1} frames")

    print("\nFrame extraction completed for all videos.")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Extract frames from videos in a specified directory and its subdirectories.')
    parser.add_argument('path', type=str, help='Absolute path to the directory containing videos')
    args = parser.parse_args()
    
    # Call the main function with the specified path
    extract_frames(args.path)