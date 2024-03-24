import asyncio
from pyppeteer import launch

async def main():
    # Launch the browser
    browser = await launch()

    # Create a new page/tab
    page = await browser.newPage()

    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    # Navigate to a webpage
    await page.goto('https://www.reddit.com/r/AmItheAsshole/')
    await page.evaluate('window.scrollTo(0, 200)')
    clip = {'x': 0, 'y': 0, 'width': 600, 'height': 300} 
    # Take a screenshot of the page
    await page.screenshot({'path': '/Users/meagan/Desktop/MDST - tiktok/W24-TikTokVideos/example.png', 'clip': clip})

    # Close the browser
    await browser.close()

# Run the async function
asyncio.get_event_loop().run_until_complete(main())