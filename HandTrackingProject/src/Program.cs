using System;
using System.Collections.Generic;
using OpenCvSharp;

namespace HandTrackingProject
{
    class Program
    {
        static void Main(string[] args)
        {
            // Initialize the HandDetector
            bool staticMode = false;
            int maxHands = 2;
            int modelComplexity = 1;
            float detectionCon = 0.5f;
            float minTrackCon = 0.5f;

            HandDetector handDetector = new HandDetector(staticMode, maxHands, modelComplexity, detectionCon, minTrackCon);

            // Capture video from the webcam
            using (var capture = new VideoCapture(0))
            {
                if (!capture.IsOpened())
                {
                    Console.WriteLine("Error: Could not open video.");
                    return;
                }

                Mat frame = new Mat();
                while (true)
                {
                    capture.Read(frame);
                    if (frame.Empty())
                    {
                        break;
                    }

                    // Find hands in the current frame
                    var hands = handDetector.FindHands(frame, true, false);

                    // Display the results
                    Cv2.ImShow("Hand Tracking", frame);

                    // Exit on 'q' key press
                    if (Cv2.WaitKey(1) == 'q')
                    {
                        break;
                    }
                }
            }

            handDetector.Dispose();
        }
    }
}