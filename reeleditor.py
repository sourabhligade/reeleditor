import moviepy.config as mp_config
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.drawing import color_gradient
import numpy as np
from moviepy.video.VideoClip import ImageClip

# Set the path to the ImageMagick binary
mp_config.IMAGEMAGICK_BINARY = "/usr/local/bin/convert"  # Adjust path as necessary

def split_video_with_text(input_video_path, output_dir, clip_duration=90):
    # Load the original video
    video = VideoFileClip(input_video_path)
    video_duration = video.duration  # Get the duration of the video in seconds

    # Calculate the number of parts
    num_parts = int(video_duration // clip_duration) + (1 if video_duration % clip_duration > 0 else 0)

    for i in range(num_parts):
        start_time = i * clip_duration
        end_time = min((i + 1) * clip_duration, video_duration)
        part = video.subclip(start_time, end_time)

        # Customize the text overlay
        top_text = f"SHAITAAN PART {i + 1}"
        
        # Create a gradient background for the text
        gradient_img = np.zeros((100, part.w, 3), dtype=np.uint8)
        gradient_img[:, :, 0] = np.linspace(65, 173, gradient_img.shape[1])  # Red channel
        gradient_img[:, :, 1] = np.linspace(105, 216, gradient_img.shape[1])  # Green channel
        gradient_img[:, :, 2] = np.linspace(225, 230, gradient_img.shape[1])  # Blue channel
        gradient_clip = ImageClip(gradient_img).set_duration(part.duration).set_fps(24)

        # Create the text clip with customizations
        top_text_clip = TextClip(top_text, fontsize=80, font='Amiri-Bold', color='white', size=gradient_clip.size)
        top_text_clip = top_text_clip.on_color(size=(top_text_clip.w + 30, top_text_clip.h + 10), color=(0, 0, 0), col_opacity=0)
        top_text_clip = top_text_clip.set_position(('center', 'top')).set_duration(part.duration).margin(top=20, opacity=0)

        # Combine the text overlay with the video part
        final_clip = CompositeVideoClip([part, gradient_clip, top_text_clip])

        # Write the resulting video part to a file
        output_path = f"{output_dir}/Part {i + 1}.mp4"
        final_clip.write_videofile(output_path, codec="libx264", fps=24)

    video.close()

# Example usage:
input_video = "/Users/sourabhligade/Desktop/reelsaved/shaitaan.mp4"  # Path to the input video
output_directory = "/Users/sourabhligade/Desktop/reelsaved"  # Directory to save the output video parts

split_video_with_text(input_video, output_directory)
