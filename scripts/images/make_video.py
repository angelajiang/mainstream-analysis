import pprint as pp
import random
import scipy.io
import shutil
import os


# Sunflowers are label 54. Image 5398 is classified incorrectly.
# ffmpeg -framerate 1 -i "%d.jpg" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"
#   ~/src/data/videos/sunflowers-dependent-1fps.mp4

def get_positive_ids(imagelabels_file, target_label):
    mat = scipy.io.loadmat(imagelabels_file)
    labels = set(mat["labels"][0])
    ids = [i for i, l in enumerate(mat["labels"][0]) \
            if l == target_label and i != 5398]
    random.shuffle(ids)
    return ids

def get_negative_ids(imagelabels_file, target_label):
    mat = scipy.io.loadmat(imagelabels_file)
    labels = set(mat["labels"][0])
    ids = [i for i, l in enumerate(mat["labels"][0]) \
            if l != target_label]
    random.shuffle(ids)
    return ids

def id_to_filename(i):
    if i < 10:
        zeroes = "0000"
    if i < 100:
        zeroes = "000"
    elif i < 1000:
        zeroes = "00"
    elif i < 10000:
        zeroes = "0"
    filename = "image_" + zeroes + str(i) + ".jpg"
    return filename

def make_video(positives, negatives, event_length_frames, non_event_length_frames,
               warmup_frames, images_dir, dst_dir):
    ordered_ids = []
    cur_positive_index = 0
    cur_negative_index = 0
    for i in range(warmup_frames):
        ordered_ids.append(positives[cur_positive_index])
    while cur_positive_index < len(positives) \
            and cur_negative_index < len(negatives):
        for i in range(event_length_frames):
            ordered_ids.append(positives[cur_positive_index])
        for i in range(non_event_length_frames):
            ordered_ids.append(negatives[cur_negative_index])
        cur_positive_index += 1
        cur_negative_index += 1

    for i, cur_id in enumerate(ordered_ids):
        orig_file = id_to_filename(cur_id)
        orig_full_file = os.path.join(images_dir, orig_file)
        dst_full_file = os.path.join(dst_dir, orig_file)

        new_file_name = str(i) + ".jpg"
        new_dst_full_file = os.path.join(dst_dir, new_file_name)

        print orig_full_file, dst_full_file
        shutil.copyfile(orig_full_file, dst_full_file)
        os.rename(dst_full_file, new_dst_full_file)


if __name__ == "__main__":
    imagelabels_file = '/Users/angela/Downloads/imagelabels.mat'
    images_dir = '/Users/angela/src/data/image-data/oxford-flowers/images/'
    dst_dir = '/Users/angela/src/data/image-data/flowers_video'
    positives = get_positive_ids(imagelabels_file, 54)
    negatives = get_negative_ids(imagelabels_file, 54)
    make_video(positives, negatives, 7, 0, 5000, images_dir, dst_dir)

