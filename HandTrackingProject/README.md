# HandTrackingProject

## Overview
The HandTrackingProject is a C# application designed for real-time hand detection and tracking using computer vision techniques. It utilizes the OpenCvSharp library to process video frames and detect hands, providing functionalities such as counting fingers and measuring distances between landmarks.

## Features
- Real-time hand detection
- Finger counting
- Distance measurement between hand landmarks
- Visualization of results on video frames

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd HandTrackingProject
   ```

2. **Install dependencies**:
   Ensure you have the necessary libraries installed. You can use NuGet to install OpenCvSharp:
   ```
   dotnet add package OpenCvSharp4
   dotnet add package OpenCvSharp4.runtime.win
   ```

3. **Build the project**:
   ```
   dotnet build
   ```

4. **Run the application**:
   ```
   dotnet run --project HandTrackingProject.csproj
   ```

## Usage
- The application will start capturing video from your webcam.
- It will detect hands in real-time and display the results on the video feed.
- You can see the number of fingers held up and the distances between specific landmarks on the hands.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.