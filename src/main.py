import time
import threading
from datetime import timedelta
import WaymoOpenDataset

if __name__=="__main__":

    training_dir = "/storage/drive_1/xinhao/our_method/data/waymo_dataset_raw/waymo_dataset_medium" # provide directory where .tfrecords are stored
    save_dir = "/storage/drive_1/xinhao/visualization/WaymoOpenDatasetToolKit/data/processed" # provide a directory where data should be extracted

    toolkit = WaymoOpenDataset.ToolKit(training_dir=training_dir, save_dir=save_dir)

    for segment in toolkit.list_training_segments():

        threads = []

        print("segment: {}".format(segment))
        toolkit.assign_segment(segment)
        start = time.time()
        t1 = threading.Thread(target=toolkit.extract_camera_images)
        t2 = threading.Thread(target=toolkit.extract_laser_images)
        t1.start()
        t2.start()
        threads.append(t1)
        threads.append(t2)
        for thread in threads:
            thread.join()
        end = time.time()
        elapsed = end - start
        print("elapsed: {}".format(elapsed))
        toolkit.save_video()
        toolkit.consolidate()
        print(timedelta(seconds=elapsed))
        break