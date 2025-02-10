
import math
import os

import cv2
import numpy as np


def detect_lanes(src_image, folder_name, side):

    src = cv2.imread(os.path.join(folder_name, src_image).replace("\\", "/"))

    src = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    scale = 1
    delta = 0
    ddepth = cv2.CV_16S

    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    grad = cv2.addWeighted(abs_grad_x, 0.2, abs_grad_y, 0.2, 0)

    #define region of interest
    height, width = grad.shape
    mask = np.zeros_like(grad)

    region_of_interest_vertices_right = [(0, height), (0, height-100), (250, height/2 + 50), (width, height-30), (width, height)]
    region_of_interest_vertices_left = [(0, height), (0, height-140), (350, height/2 + 50), (width, height-30), (width, height)]

    if side == "left":
        region_of_interest = region_of_interest_vertices_left
    else:
        region_of_interest = region_of_interest_vertices_right    

    cv2.fillPoly(mask, np.array([region_of_interest], np.int32), 255)

    grad = cv2.bitwise_and(grad, mask)

    #add threshold
    _,binary_image = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #apply hough transform
    lines = cv2.HoughLines(binary_image, rho=1, theta=np.pi/180, threshold=100)

    #seperate left and right lane edges
    lef_lines, right_lines = seperate_lines(lines)

    #draw average lines and intercept
    annotated_image = draw_average_line(lef_lines, right_lines, src)

    #save image
    folder_path = f"processed_images_{side}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    final_path = os.path.join(folder_path, f"{src_image}_masked.bmp".replace("\\", "/"))
    print(final_path)
    cv2.imwrite(final_path, annotated_image)
    
def seperate_lines(lines):
    left_lines = []
    right_lines = []
    
    for line in lines:
        #calculate the slope
        _, theta = line[0] #rho, theta
        slope = -math.cos(theta) / math.sin(theta)
        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)
    
    return left_lines, right_lines

def get_intercept_coordinates(left_x1, left_y1, left_x2, left_y2, right_x1, right_y1, right_x2, right_y2):
     # Compute the intersection point
    left_slope = (left_y2 - left_y1) / (left_x2 - left_x1)
    right_slope = (right_y2 - right_y1) / (right_x2 - right_x1)
    left_intercept = left_y1 - left_slope * left_x1
    right_intercept = right_y1 - right_slope * right_x1
    x = int((right_intercept - left_intercept) / (left_slope - right_slope))
    y = int(left_slope * x + left_intercept)

    return x, y

def draw_average_line(left_lines, right_lines, src_image):
    # Variables to store the sum of rho and theta
    sum_rho = 0
    sum_theta = 0
    num_lines = len(left_lines)

    # Loop through each detected line
    for line in left_lines:
        rho, theta = line[0]  # Unpack rho and theta
        sum_rho += rho
        sum_theta += theta

    # Compute the average rho and theta
    avg_rho = sum_rho / num_lines
    avg_theta = sum_theta / num_lines

    # Draw the average line
    a = np.cos(avg_theta)
    b = np.sin(avg_theta)
    x0 = a * avg_rho
    y0 = b * avg_rho
    left_x1 = int(x0 + 1000 * (-b))
    left_y1 = int(y0 + 1000 * (a))
    left_x2 = int(x0 - 1000 * (-b))
    left_y2 = int(y0 - 1000 * (a))

    #right lines
    sum_rho = 0
    sum_theta = 0
    num_lines = len(right_lines)

    # Loop through each detected line
    for line in right_lines:
        rho, theta = line[0]  # Unpack rho and theta
        sum_rho += rho
        sum_theta += theta

    # Compute the average rho and theta
    avg_rho = sum_rho / num_lines
    avg_theta = sum_theta / num_lines

    # Draw the average line
    a = np.cos(avg_theta)
    b = np.sin(avg_theta)
    x0 = a * avg_rho
    y0 = b * avg_rho
    right_x1 = int(x0 + 1000 * (-b))
    right_y1 = int(y0 + 1000 * (a))
    right_x2 = int(x0 - 1000 * (-b))
    right_y2 = int(y0 - 1000 * (a))

    #get intercept coordinates
    intercept_x, intercept_y = get_intercept_coordinates(left_x1, left_y1, left_x2, left_y2, right_x1, right_y1, right_x2, right_y2)

    #draw left lane
    cv2.line(src_image, (left_x1, left_y1), (intercept_x, intercept_y), (0, 255, 0), 4)

    #draw right lane
    cv2.line(src_image, (intercept_x, intercept_y), (right_x2, right_y2), (0, 255, 0), 4)

    #draw intercept
    cv2.circle(src_image, (intercept_x, intercept_y), 6, (0, 0, 255), -1)

    return src_image

def generate_video(folder_name):
    images = [img for img in os.listdir(folder_name) if img.endswith(".bmp")]
    #sort images according to name
    images.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    frame = cv2.imread(os.path.join(folder_name, images[0]).replace("\\", "/"))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(f"{folder_name}.mp4", fourcc, 15, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(folder_name, image).replace("\\", "/")))

    cv2.destroyAllWindows()
    video.release()

    return 0

def main():

    #left image processing
    folder_name = "TestVideo_2"
    images = [img for img in os.listdir(folder_name) if img.endswith(".bmp")]
    for image in images:
        print(image, folder_name)
        detect_lanes(image, folder_name, "left")

    #generate video
    generate_video("processed_images_left")
    
    #right image processing
    folder_name = "TestVideo_1"
    images = [img for img in os.listdir(folder_name) if img.endswith(".bmp")]
    for image in images:
        print(image, folder_name)
        detect_lanes(image, folder_name, "right")
    
    #generate video
    generate_video("processed_images_right")

    return 0

if __name__ == "__main__":
    main()