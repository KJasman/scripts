import cv2  # OpenCV library for video processing
import os  # For file and directory operations
from typing import List, Tuple  # For type hinting
import argparse  # For parsing command-line arguments
import concurrent.futures  # For multithreading support
import multiprocessing  # For getting CPU count

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
    Process a single video file: extract frames at regular intervals and save them as JPEG images.
    
    Args:
    video_file (str): Path to the video file to process.
    base_path (str): The original base path used to maintain directory structure.
    stills_base_path (str): The base path where extracted frames will be saved.
    
    Returns:
    str: A message indicating the number of frames extracted from the video.
"""
def process_video(video_file: str, base_path: str, stills_base_path: str) -> str:
    print(f"Processing video: {os.path.basename(video_file)}")
    
    # Open the video file
    video = cv2.VideoCapture(video_file)
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate frame interval (extract a frame every 5 seconds)
    frame_interval = round(5.0 * fps)
    frame_counter = 0
    image_index = 1
    
    # Create a subdirectory for this video's frames, maintaining the original directory structure
    relative_path = os.path.relpath(video_file, base_path)
    video_stills_path = os.path.join(stills_base_path, os.path.dirname(relative_path), os.path.splitext(os.path.basename(video_file))[0])
    os.makedirs(video_stills_path, exist_ok=True)
    
    # Process frames
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
    
    # Close the video file
    video.release()
    
    completion_message = f"Completed processing {os.path.basename(video_file)}. Extracted {image_index-1} frames."
    print(completion_message)
    return completion_message

"""
    Extract frames from all video files in the specified directory and its subdirectories.
    This function uses multithreading to process multiple videos concurrently.
    
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
    
    # Determine the number of threads to use (equal to the system's logical CPU count)
    max_threads = max(1, multiprocessing.cpu_count())
    print(f"Using {max_threads} threads for video processing")
    
    # Use a ThreadPoolExecutor to process videos concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all video processing tasks to the executor
        futures = [executor.submit(process_video, video_file, base_path, stills_base_path) for video_file in video_files]
        
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    
    print("\nFrame extraction completed for all videos.")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Extract frames from videos in a specified directory and its subdirectories using multiple threads.')
    parser.add_argument('path', type=str, help='Absolute path to the directory containing videos')
    args = parser.parse_args()
    
    # Call the main function with the specified path
    extract_frames(args.path)