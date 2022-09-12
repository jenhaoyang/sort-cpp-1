#pragma once

#include <opencv2/core.hpp>
#include "kalman_filter.h"
#include <pybind11/numpy.h>

namespace py = pybind11;

class Track {
public:
    // Constructor
    Track();

    // Destructor
    ~Track() = default;

    void Init(const cv::Vec6i& bbox);
    void Predict();
    void Update(const cv::Rect& bbox);
    cv::Rect GetStateAsBbox() const;
    py::array_t<int> GetStateAsBboxArray() const;
    float GetNIS() const;

    int coast_cycles_ = 0, hit_streak_ = 0;
    int confidence = -1;
    int obj_type = -1;

private:
    Eigen::VectorXd ConvertBboxToObservation(const cv::Rect& detail_bbox) const;
    cv::Rect ConvertStateToBbox(const Eigen::VectorXd &state) const;

    KalmanFilter kf_;
};
cv::Rect convert_single_rect(const cv::Vec6i& detail_detections);