#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

char key;
int index = 0;

int main( int argc, char** argv )
{
	
	cvNamedWindow("Camera_Output", 1);    //Create window
    CvCapture* capture = cvCaptureFromCAM(CV_CAP_ANY);  //Capture using any camera connected to your system
    while(1){ //Create infinte loop for live streaming
 
        IplImage* frame = cvQueryFrame(capture); //Create image frames from capture
        cvShowImage("Camera_Output", frame);   //Show image frames on created window
        key = cvWaitKey(10);     //Capture Keyboard stroke
        if (char(key) == 27){
            
			
			break;      //If you hit ESC key loop will break.
        }
		else if(char(key) == 32){//if space bar is pressed
			IplImage *img=cvQueryFrame(capture);

			stringstream ss; //to convert int to string;
			String imageName("image");	
			
			//convert int to string
			ss << index;
			string str = ss.str();
			cout << str << endl;
			imageName.append(str);
			imageName.append(".jpg");
			index++;
			// Save the frame into a file
			cvSaveImage(imageName.c_str(),img);
			cout << "Image saved" <<endl;			
		}
		
		
    }
    cvReleaseCapture(&capture); //Release capture.
    cvDestroyWindow("Camera_Output"); //Destroy Window
    return 0;
}