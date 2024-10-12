import pyrealsense2 as rs
import numpy as np

# Create a pipeline
pipeline = rs.pipeline()

# Start streaming with default configuration
pipeline.start()

# Get the intrinsics of the color stream
try:
    # Wait for a frame to be ready
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    
    # Get the stream profile for the color stream
    color_profile = color_frame.get_profile()
    
    # Get the intrinsics
    intrinsics = color_profile.as_video_stream_profile().get_intrinsics()
    
    # Convert intrinsics to a matrix
    K = np.array([
        [intrinsics.fx, 0, intrinsics.ppx],
        [0, intrinsics.fy, intrinsics.ppy],
        [0, 0, 1]
    ])
    
    print("Intrinsic Matrix K:")
    print(K)
finally:
    # Stop streaming
    pipeline.stop()
