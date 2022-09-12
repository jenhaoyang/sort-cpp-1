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
    import scikit_build_example
    from pathlib import Path
    import time
    dataset_names = ["ADL-Rundle-6", "ADL-Rundle-8", "ETH-Bahnhof",
                    "ETH-Pedcross2", "ETH-Sunnyday", "KITTI-13",
                    "KITTI-17", "PETS09-S2L1", "TUD-Campus",
                    "TUD-Stadtmitte", "Venice-2"]

    tracker = scikit_build_example.Tracker()

    dataset_name  = dataset_names[2]
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
                    out_file.write(f"{frame_index+1},{obj_index},{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},,1,-1,-1,-1\n")

        end = time.time()
        time_span = end - start
    total_frames = len(all_detections)
    print(F"FPS:{total_frames / time_span}")