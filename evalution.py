import numpy as np
kMinHits = 3
kMinConfidence = 0.6
kMaxCoastCycles = 1

def ProcessLabel(label_file):
    # Process labels - group bounding boxes by frame index
    bbx = []
    bbox_per_frame = []
    current_frame_index = 1
    

    with open(label_file) as label_f:
        lines = label_f.readlines()

    for line in lines:
        # Label format <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
        label_data = line.split(",")
        if int(label_data[0]) != current_frame_index:
            current_frame_index = int(label_data[0])
            bbx.append(bbox_per_frame)
            bbox_per_frame = []

        if float(label_data[6]) > kMinConfidence :
            bbx_string = label_data[2:6]
            bbox_per_frame.append(np.array([float(data) for data in bbx_string])) 
    
    # Add bounding boxes from last frame
    bbx.append(bbox_per_frame)
    return bbx

if __name__ == "__main__":
    import cppsort
    from pathlib import Path
    import time
    dataset_names = ["ADL-Rundle-6", "ADL-Rundle-8", "ETH-Bahnhof",
                    "ETH-Pedcross2", "ETH-Sunnyday", "KITTI-13",
                    "KITTI-17", "PETS09-S2L1", "TUD-Campus",
                    "TUD-Stadtmitte", "Venice-2"]

    #tracker = cppsort.Tracker()

    for dataset_name in dataset_names:
        tracker = cppsort.Tracker()
        # Open label file and load detections from MOT dataset
        # Note that it can also be replaced by detections from you own detector
        label_path = f"data/{dataset_name}/det.txt"

        all_detections = ProcessLabel(label_path)

        # Create output folder if it does not exist
        output_folder = Path("output")
        if output_folder.exists() == False:
            output_folder.mkdir()

        output_path = output_folder / f"{dataset_name}.txt"
        with open(output_path, "w") as out_file:
            start = time.time()

            for frame_index, detections in enumerate(all_detections):
                tracker.Run(detections)
                tracks:dict = tracker.GetTracks()


                for obj_index, track in tracks.items():
                    bbox = track.GetStateAsBboxArray()
                    # Note that we will not export coasted tracks
                    # If we export coasted tracks, the total number of false negative will decrease (and maybe ID switch)
                    # However, the total number of false positive will increase more (from experiments),
                    # which leads to MOTA decrease
                    # Developer can export coasted cycles if false negative tracks is critical in the system
                    if (track.coast_cycles_ < kMaxCoastCycles) and (track.hit_streak_ >= kMinHits or frame_index < kMinHits):
                        out_file.write(f"{frame_index+1},{float(obj_index)},{float(bbox[0])},{float(bbox[1])},{float(bbox[2])},{float(bbox[3])},1,-1,-1,-1\n")

            end = time.time()
            time_span = end - start
        total_frames = len(all_detections)
        print(F"FPS:{total_frames / time_span}")
        tracker = None


# if __name__ == '__main__':
#     # all train
#     import os
#     from sort import *
#     total_time = 0.0
#     total_frames = 0


#     if not os.path.exists('output'):
#         os.makedirs('output')

#     mot_tracker = Sort(max_age=1, 
#                        min_hits=3,
#                        iou_threshold=0.6) #create instance of the SORT tracker
#     seq_dets = np.loadtxt("/home/ai_server/2005013/ai_surve/sort-cpp-1/data/ETH-Bahnhof/det.txt", delimiter=',')
#     seq = "ETH-Bahnhof"
#     with open(os.path.join('output', '%s.txt'%(seq)),'w') as out_file:
#       print("Processing %s."%(seq))
#       for frame in range(int(seq_dets[:,0].max())):
#         frame += 1 #detection and frame numbers begin at 1
#         dets = seq_dets[seq_dets[:, 0]==frame, 2:7]
#         dets[:, 2:4] += dets[:, 0:2] #convert to [x1,y1,w,h] to [x1,y1,x2,y2]
#         total_frames += 1

#         start_time = time.time()
#         trackers = mot_tracker.update(dets)
#         cycle_time = time.time() - start_time
#         total_time += cycle_time

#         for d in trackers:
#           print('%d,%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1'%(frame,d[4],d[0],d[1],d[2]-d[0],d[3]-d[1]),file=out_file)

#     print("Total Tracking took: %.3f seconds for %d frames or %.1f FPS" % (total_time, total_frames, total_frames / total_time))
