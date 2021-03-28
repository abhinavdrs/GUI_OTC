from video_class import VideoPlayer

# Create video player object
video_player = VideoPlayer()

# Browse the file system to load the video
video_player.browse_video()

# Initialize OpenCV video_reader object (vidFile) and return [vidFile_object, num_frames, fps]
video_player.get_video()

# Initialize and return layout for video player
layout = video_player.video_layout()

# Initialize windows for video player
video_player.video_window()

# Final function to call the event loop.
#To Do: pass event and value from the main app to this app.
video_player.show_video()
