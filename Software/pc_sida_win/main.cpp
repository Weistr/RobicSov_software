#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
using namespace cv;
int main()
{
    Mat img = imread("C:/Users/15612/Documents/Project/RobicSov_R1/RobicSov/Software/pc_sida_win/imgs/opencv.jpeg");
    imshow("image", img);
    waitKey();
    return 0;
}