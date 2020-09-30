import os
import glob


if __name__ == "__main__":
    live_path = "/home/dmp/PRNet-Depth-Generation/train/live"
    depth_live_path = "/home/dmp/PRNet-Depth-Generation/train/live_depth"
    image_in_live = glob.glob(live_path + "/*")
    image_in_depth = glob.glob(depth_live_path + "/*")
    print(len(image_in_live), len(image_in_depth))
    name_in_live = set()
    for path_in_live in image_in_live:
        img_name = os.path.basename(path_in_live)
        name = os.path.splitext(img_name)[0]
        name_in_live.add(name)
    count = 0
    for path_in_depth in image_in_depth:
        img_name = os.path.basename(path_in_depth)
        name = os.path.splitext(img_name)[0]
        if name in name_in_live:
            continue
        os.remove(path_in_depth)
        # print("have removed file {}".format(path_in_depth))
        count+=1
    print(count)

    