const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Create screenshots directory if it doesn't exist
const screenshotsDir = path.join(__dirname, 'screenshots');
if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir);
}

async function monitorTraffic(url, monitorTime = 30000) { // Default 30 seconds monitoring
    console.log('Launching browser...');
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: [
            '--start-maximized',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process'
        ],
        ignoreHTTPSErrors: true
    });

    console.log('Creating new page...');
    const page = await browser.newPage();

    // Set a longer timeout
    page.setDefaultNavigationTimeout(60000);
    page.setDefaultTimeout(60000);

    // Enable request interception
    await page.setRequestInterception(true);

    // Log all requests
    page.on('request', request => {
        const url = request.url();
        console.log(`Request: ${request.method()} ${url}`);
        request.continue();
    });

    // Log all responses
    page.on('response', response => {
        const url = response.url();
        console.log(`Response: ${response.status()} ${url}`);
    });

    // Log console messages
    page.on('console', msg => {
        console.log('Console:', msg.text());
    });

    // Log page errors
    page.on('pageerror', error => {
        console.error('Page Error:', error.message);
    });

    // Log request failures
    page.on('requestfailed', request => {
        console.error('Request Failed:', request.url(), request.failure().errorText);
    });

    try {
        console.log(`Navigating to ${url}...`);
        const response = await page.goto(url, {
            waitUntil: ['domcontentloaded', 'networkidle0'],
            timeout: 60000
        });

        console.log('Navigation completed. Status:', response.status());
        
        // Take a screenshot
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        await page.screenshot({
            path: path.join(screenshotsDir, `screenshot-${timestamp}.png`),
            fullPage: true
        });

        console.log(`Monitoring for ${monitorTime/1000} seconds...`);
        
        // Monitor for the specified time using setTimeout
        await new Promise((resolve, reject) => {
            setTimeout(async () => {
                try {
                    console.log('Monitoring complete. Taking final screenshot...');
                    const finalTimestamp = new Date().toISOString().replace(/[:.]/g, '-');
                    await page.screenshot({
                        path: path.join(screenshotsDir, `final-${finalTimestamp}.png`),
                        fullPage: true
                    });
                    console.log('Closing browser...');
                    await browser.close();
                    resolve();
                } catch (error) {
                    reject(error);
                }
            }, monitorTime);
        });

        process.exit(0);
    } catch (error) {
        console.error('Error:', error);
        // Take a screenshot even if there's an error
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        await page.screenshot({
            path: path.join(screenshotsDir, `error-${timestamp}.png`),
            fullPage: true
        });
        await browser.close();
        process.exit(1);
    }
}

// Example usage
const targetUrl = 'https://www.houstontx.gov/solidwaste/';
monitorTraffic(targetUrl, 30000).catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
}); 