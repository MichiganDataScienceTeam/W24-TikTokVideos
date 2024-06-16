import json
from playwright.sync_api import ViewportSize, sync_playwright
from PIL import Image, ImageDraw
import time
import os

VIEWPORT = {"width": 2560, "height": 1440}
DEVICE_SCALE_FACTOR = 2


def screenshot(url: str, nsfw: bool, filename: str, credentials: dict):
    print("Capture Screenshot at:")
    print(f"https://publish.reddit.com/embed?url={url}?snippet=")
    print(f"Save to: screenshot/{filename}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        if os.path.exists("state.json"):
            context = browser.new_context(
                storage_state="state.json",
                viewport=VIEWPORT,
                device_scale_factor=DEVICE_SCALE_FACTOR,
            )
        else:
            context = browser.new_context(
                locale="en-us",
                viewport=VIEWPORT,
                device_scale_factor=DEVICE_SCALE_FACTOR,
            )
            with open("cookies.json") as file:
                cookies = json.load(file)
                context.add_cookies(cookies)
            login(context, credentials)

        page = context.new_page()
        page.goto(f"https://publish.reddit.com/embed?url={url}?snippet=", timeout=0)
        # page.set_viewport_size(ViewportSize(width=W, height=H))
        page.wait_for_load_state()

        iframe = page.frame_locator("iFrame")
        if iframe is None:
            print("Iframe not found")
            return

        time.sleep(5)

        expand_button = iframe.locator("button#t3_1qzlo4-read-more-button")

        if expand_button.is_visible():
            expand_button.click()
            print("Clicked the 'Read more' button.")
        else:
            print("The 'Read more' button was not found or not visible.")

        nsfw_button = iframe.locator('button:has-text("View")')

        if nsfw_button.is_visible():
            nsfw_button.click()
            print("Clicked the 'View' button.")
        else:
            print("The 'View' button was not found or not visible.")

        page.locator("iframe").screenshot(path="temp/" + filename)
        round_corners("temp/" + filename, "screenshot/" + filename)


def login(context, credentials: dict):
    page = context.new_page()
    page.goto("https://www.reddit.com/login", timeout=0)
    page.set_viewport_size(ViewportSize(width=700, height=700))
    page.wait_for_load_state()

    page.locator("input#login-username").fill(credentials["reddit_username"])
    page.locator("input#login-password").fill(credentials["reddit_password"])
    page.get_by_role("button", name="Log In").click()

    login_error_div = page.locator(".AnimatedForm__errorMessage").first

    if login_error_div.is_visible():
        login_error_message = login_error_div.inner_text()
        if login_error_message.strip() == "":
            # The div element is empty, no error
            pass
        else:
            # The div contains an error message
            exit()

    # Save storage state into the file.
    context.storage_state(path="state.json")


def round_corners(input_image_path, output_image_path, corner_radius=16):
    image = Image.open(input_image_path).convert("RGBA")

    width, height = image.size
    rounded_mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(rounded_mask)

    draw.rounded_rectangle([(0, 0), (width, height)], radius=corner_radius, fill=255)

    rounded_image = Image.new("RGBA", (width, height))
    rounded_image.paste(image, (0, 0), mask=rounded_mask)

    rounded_image.save(output_image_path, format="PNG")


if __name__ == "__main__":
    screenshot(
        "https://www.reddit.com/r/AskReddit/comments/1bfblld/whats_a_dirty_little_secret_that_you_know_only/",
        True,
    )
