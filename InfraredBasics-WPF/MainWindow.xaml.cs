using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Windows;
using System.Windows.Media.Imaging;
using Microsoft.Kinect;
using System.Diagnostics;
using System.Windows.Media;

namespace Microsoft.Samples.Kinect.InfraredBasics
{
    public partial class MainWindow : Window
    {
        private KinectSensor sensor;
        private WriteableBitmap colorBitmap;
        private byte[] colorPixels;

        private TcpClient tcpClient;
        private NetworkStream networkStream;
        private const string serverIp = "127.0.0.1";
        private const int serverPort = 5052;

        public MainWindow()
        {
            InitializeComponent();
            AllocConsole();
        }

        [System.Runtime.InteropServices.DllImport("kernel32.dll")]
        private static extern bool AllocConsole();

        private void WindowLoaded(object sender, RoutedEventArgs e)
        {
            // Look through all sensors and start the first connected one
            foreach (var potentialSensor in KinectSensor.KinectSensors)
            {
                if (potentialSensor.Status == KinectStatus.Connected)
                {
                    this.sensor = potentialSensor;
                    break;
                }
            }

            if (null != this.sensor)
            {
                this.sensor.ColorStream.Enable(ColorImageFormat.InfraredResolution640x480Fps30);
                this.colorPixels = new byte[this.sensor.ColorStream.FramePixelDataLength];
                this.colorBitmap = new WriteableBitmap(this.sensor.ColorStream.FrameWidth, this.sensor.ColorStream.FrameHeight, 96.0, 96.0, PixelFormats.Gray16, null); // Updated line
                this.Image.Source = this.colorBitmap;
                this.sensor.ColorFrameReady += this.SensorColorFrameReady;

                try
                {
                    this.sensor.Start();
                }
                catch (IOException)
                {
                    this.sensor = null;
                }

                // Establish a TCP connection to the server
                tcpClient = new TcpClient(serverIp, serverPort);
                networkStream = tcpClient.GetStream();
            }

            if (null == this.sensor)
            {
                this.statusBarText.Text = InfraredBasics_WPF.Properties.Resources.NoKinectReady;
            }
        }

        private void WindowClosing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (sensor != null)
            {
                sensor.Stop();
            }
            if (tcpClient != null)
            {
                networkStream.Close();
                tcpClient.Close();
            }
        }

        private void SensorColorFrameReady(object sender, ColorImageFrameReadyEventArgs e)
        {
            using (ColorImageFrame colorFrame = e.OpenColorImageFrame())
            {
                if (colorFrame != null)
                {
                    colorFrame.CopyPixelDataTo(this.colorPixels);

                    this.colorBitmap.WritePixels(
                        new Int32Rect(0, 0, this.colorBitmap.PixelWidth, this.colorBitmap.PixelHeight),
                        this.colorPixels,
                        this.colorBitmap.PixelWidth * colorFrame.BytesPerPixel,
                        0);

                    SendInfraredData(this.colorPixels);
                }
            }
        }

        private void SendInfraredData(byte[] infraredData)
        {
            try
            {
                // Write the image data to the TCP stream
                Console.WriteLine($"Sending {infraredData.Length} bytes...");

                // Send the data in one go over the TCP stream
                networkStream.Write(infraredData, 0, infraredData.Length);
                networkStream.Flush();

                Console.WriteLine("Image data sent successfully!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error sending data: {ex.Message}");
            }
        }
    }
}
