# lane-detection
detect lanes of a road using dash a cam video. Used Sobel edge detection and Hough transformation

## Model based lane detection

Find two line models of lane markers, one from the left size and the other from the right side of the current vehicle.

![image](https://user-images.githubusercontent.com/7046889/198094792-7992c1e4-3729-4484-9b03-beb5a606380b.png)

To simplify the detection problem, we assume the following constraints
   1. Only two lane markers will be detected (line1, line2)
   2. Only interest area below of certain ```y``` value will be processed. 
   3. Line1 has negative slope (-0.5~-1.5), while line2 has positive slope (0.5~1.5).

![image](https://user-images.githubusercontent.com/7046889/198095755-b81086c1-c90c-4886-adcf-5b4880b38654.png)

## Detection steps

  1. Convert an input image to a grayscale image
  2. Apply Sobel edge detection algorithm 

![image](https://user-images.githubusercontent.com/7046889/198096068-dab3c791-bfbb-411a-b7a5-4781c2003d26.png)

  3. From the vehicle’s current center (x position), search the first edge pixel in each left and right direction (Do it in all scanlines). The edge angle of the first edge pixel from the vehicle center is 0 degree in the right side, and 180 degree in the left side. 

![image](https://user-images.githubusercontent.com/7046889/198096585-dc5da48f-783d-4034-a773-09300083cd01.png)
![image](https://user-images.githubusercontent.com/7046889/198097149-60a57e94-0743-4019-9ccc-bb678cd82dac.png)

  4. Using the edge pixels, apply the Hough transform to determine the two line models.
  
![image](https://user-images.githubusercontent.com/7046889/198097248-cef4a660-dbdd-444d-80a3-a33b26c52082.png)

  5. Draw two lines over the original road image. At the intersection of the lines, draw a circle which represents the vanishing point.  Draw the two lines from the image border to the vanishing point.  
  
![image](https://user-images.githubusercontent.com/7046889/198098128-2db5a1b4-491b-4231-a814-1aef0157fbb1.png)

  6. Apply the same lane detection algorithm to other video frames. 
  
  
## Submissions 

Due: 31 October 2400 h

Submission: Source codes, report explaing the code and including input and output images, video file for two test sets. 



  
