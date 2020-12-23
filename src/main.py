import cv2
from skimage.metrics import structural_similarity
import imutils
from selenium import webdriver
import subprocess
import os
import requests



def screenshot(driver, url, filename):
    # ローカルホスト指定はホストマシンのIPに書き換える
    if "localhost" in url:
        host_addr = subprocess.run(["ip route | awk 'NR==1 {print $3}'"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True).stdout.decode("utf8").rstrip('\n')
        url = url.replace("localhost", host_addr)
    driver.get(url)
    driver.save_screenshot(filename)


def diff_images(base_image_path, compare_image_path, diff_image_path):
    """
    referer to https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    :param base_image_path:
    :param compare_image_path:
    :param diff_image_path:
    :return:
    """
    # load the two input images
    base_image = cv2.imread(base_image_path)
    compare_image = cv2.imread(compare_image_path)

    # convert the images to grayscale
    grayA = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(compare_image, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(base_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(compare_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imwrite(base_image_path, base_image)
    cv2.imwrite(compare_image_path, compare_image)
    cv2.imwrite(diff_image_path, diff)

def post_image(path, text):
    file =  {
        'file': (path, open(path, 'rb'), 'png')
    }
    payload = {
        "token": os.environ['SLACK_TOKEN'],
        "channels": os.environ['SLACK_CHANNEL'],
        "title": text
    }

    response = requests.post(url="https://slack.com/api/files.upload", params=payload, files=file)
    print(response.json())

def main():
    dist_path = "/app/dist"
    base_image_path = f"{dist_path}/base.png"
    compare_image_path = f"{dist_path}/compare.png"
    diff_image_path = f"{dist_path}/diff.png"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--window-size={}'.format(os.environ['WINDOW_SIZE']))

    driver = webdriver.Chrome(options=options)
    screenshot(driver, os.environ['BASE_URL'], base_image_path)
    screenshot(driver, os.environ['COMPARE_URL'], compare_image_path)
    diff_images(base_image_path, compare_image_path, diff_image_path)
    driver.close()
    driver.quit()

    post_image(base_image_path, "Original Image")

    post_image(compare_image_path, "Compare Image")

    if os.getenv('ENABLE_SHOW_DIFF', 'NO') == 'YES':
        post_image(diff_image_path, "Difference Image")




if __name__ == '__main__':
    main()
