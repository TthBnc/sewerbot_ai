import cv2
import os

def slice_video(video_name_ext, frame_interval, path, write_path = 'C:\\_TBZ mindenes\\sewerbot_ai\\src\\pictures\\temp'):
    video_name = video_name_ext[:-4]

    write_path = os.path.join(write_path, video_name)
    
    if not os.path.exists(write_path):
        os.makedirs(write_path)
        
    video_path = os.path.join(path, video_name_ext)
    video = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        ret, frame = video.read()

        if not ret:
            print(f'end of the video: {video_name}')
            break

        frame_count += 1

        if (frame_count % frame_interval == 0):
            filename = f'{video_name}_{frame_count//frame_interval}.jpg'
            file_path = os.path.join(write_path, filename)
            # print(file_path)
            if frame is None:
                print(f'frame is None')
            else:
                cv2.imwrite(file_path, frame)

    video.release()

def delete_temp_contents(temp_folder='C:\\_TBZ mindenes\\sewerbot_ai\\src\\pictures\\temp'):
    try:
        files_deleted = 0
        folders_deleted = 0
        temp_contents = os.listdir(temp_folder)

        for item in temp_contents:
            item_path = os.path.join(temp_folder, item)

            if os.path.isfile(item_path):
                os.remove(item_path)
                files_deleted += 1

            elif os.path.isdir(item_path):
                os.rmdir(item_path)
                folders_deleted += 1

        
        print(f'Filed deleted: {files_deleted}')
        print(f'Folders deleted: {folders_deleted}')
        print(f'Contents in {temp_folder} have been deleted.')
    except Exception as e:
        print(f'Error deleting contents in {temp_folder}: {e}')


def process_video(video_name_ext, frame_interval=1, src=None, special_frames=None, throwaway_frames=None, base_write_path=None):
    if src is None:
        src = 'C:\\_TBZ mindenes\\sewerbot_ai\\src\\videos'
    if special_frames is None:
        special_frames = []
    if throwaway_frames is None:
        throwaway_frames = []

    video_name = video_name_ext[:-4]
    video_path = os.path.join(src, video_name_ext)
    video = cv2.VideoCapture(video_path)

    frame_count = 0

    while True:
        ret, frame = video.read()

        if not ret:
            print('end of the video')
            break

        frame_count += 1
        not_in_range = True
        throwaway = False
        filename = ''

        if (frame_count % frame_interval == 0):
            for start, end in throwaway_frames:
                if end >= frame_count >= start:
                    throwaway = True
            if not throwaway:
                for start, end in special_frames:
                    if end >= frame_count >= start:
                        filename = f'end_{video_name}_{frame_count//frame_interval}.jpg'
                        write_path = os.path.join(base_write_path, "end")
                        # write_path = 'C:\\_TBZ mindenes\\sewerbot_ai\\src\\pictures\\data\\end'
                        not_in_range = False
                if not_in_range:
                    filename = f'notEnd_{video_name}_{frame_count//frame_interval}.jpg'
                    write_path = os.path.join(base_write_path, 'notEnd')
                    # write_path = 'C:\\_TBZ mindenes\\sewerbot_ai\\src\\pictures\\data\\notEnd'
                file_path = os.path.join(write_path, filename)
                cv2.imwrite(file_path, frame)

    video.release()


import torch
def save_model(epoch, model, optimizer, filename, isCheckpoint=False):
    """
    usage:
        save_checkpoint(epoch, gen, opt_gen, "generator_checkpoint.pth")
        save_checkpoint(epoch, critic, opt_critic, "critic_checkpoint.pth")
    """
    if isCheckpoint:
        path = os.path.join("models", "checkpoints", filename + '.pth')
    else:
        path = os.path.join("models", filename + '.pth')

    checkpoint = {
        "epoch": epoch,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
    }
    if isCheckpoint: print('=> Saving checkpoint')
    else: print('=> Saving model')
    torch.save(checkpoint, path)

def load_model(model, optimizer, filename):
    """
    usage:
        start_epoch = load_checkpoint(gen, opt_gen, "generator_checkpoint.pth")
        start_epoch = max(start_epoch, load_checkpoint(critic, opt_critic, "critic_checkpoint.pth"))

        for epoch in range(start_epoch, NUM_EPOCHS):
            # ...
            # your training code here
            # ...
    """
    
    checkpoint = torch.load(filename)
    model.load_state_dict(checkpoint["model_state"])
    optimizer.load_state_dict(checkpoint["optimizer_state"])
    return checkpoint["epoch"]  # You can use this to know where the training left off