from moviepy.editor import VideoFileClip
import shutil
import os


def resize_video(
    input_path: str,
    output_path: str,
    target_resolution: tuple[int],
    overwrite: bool = False,
):
    if not overwrite and os.path.exists(output_path):
        print("Resize Cache", output_path)
        return
    video_clip = VideoFileClip(input_path)

    target_width, target_height = target_resolution
    if target_width == video_clip.w and target_height == video_clip.h:
        if input_path != output_path:
            shutil.copy(input_path, output_path)
        return

    target_aspect_ratio = target_width / target_height
    original_aspect_ratio = video_clip.aspect_ratio

    if original_aspect_ratio > target_aspect_ratio:
        scaling_factor = target_height / video_clip.h
        new_width = int(video_clip.w * scaling_factor)
        new_height = target_height
    else:
        scaling_factor = target_width / video_clip.w
        new_width = target_width
        new_height = int(video_clip.h * scaling_factor)

    resized_clip = video_clip.resize((new_width, new_height))

    x_offset = (new_width - target_width) // 2
    y_offset = (new_height - target_height) // 2

    cropped_clip = resized_clip.crop(
        x1=x_offset,
        y1=y_offset,
        x2=x_offset + target_width,
        y2=target_height + y_offset,
    )

    print(cropped_clip.w, cropped_clip.h)
    cropped_clip.write_videofile(output_path, codec="libx264")
    video_clip.close()
    resized_clip.close()
    cropped_clip.close()


if __name__ == "__main__":
    target_resolution = (720, 1280)
    files = os.listdir("backgrounds")
    for file in files:
        file_path = os.path.join("backgrounds", file)
        out_path = os.path.join("backgrounds", "resize-" + file)
        if file.startswith("resize-"):
            continue

        print(file_path)
        if os.path.isfile(file_path):
            try:
                resize_video(file_path, out_path, target_resolution)
            except Exception as e:
                print(e)
                continue
